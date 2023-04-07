const selfURL = "https://api.www.documentcloud.org/api/users/me/";
const searchURL = "https://api.www.documentcloud.org/api/documents/search?q=*:*&order_by=created_at";


// Constants
// TODO: Custom scrollbar?
const yearHeight = 64;
const monthHeight =
  (window.innerHeight -
    document
      .querySelector('.month-map-container .title')
      .getBoundingClientRect().height) /
  12;
const dayHeight = 64;
const maxBarLength = 200;
const dayTimelineHeight = 365 * dayHeight;

var englishMonthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December',
];

// State
var occsByYear = {};
var dayGroupsByDateStringByYear = {};
var mostOccsInAYear = 0;
var sortedOccs = {};

function populateOccsDict(occs) {
  occs.forEach(putInYearDict);
  occs.forEach(putInDayGroup);
  var sortedOccs = Object.keys(occsByYear).sort();
  if (sortedOccs.length < 1) {
    throw new Error('No years found in data.');
  }

  return sortedOccs;

  // Side effect: Updates mostOccsInAYear.
  function putInYearDict(occ) {
    const year = new Date(occ.entity.date).getFullYear();
    var occsForYear = occsByYear[year];
    if (!occsForYear) {
      occsForYear = [];
      occsByYear[year] = occsForYear;
    }
    occsForYear.push(occ);
    occsForYear.sort((a, b) => (a.entity.date < b.entity.date ? -1 : 1));

    if (occsForYear.length > mostOccsInAYear) {
      mostOccsInAYear = occsForYear.length;
    }

    var dayGroupsForYear = dayGroupsByDateStringByYear[year];
    if (!dayGroupsForYear) {
      dayGroupsForYear = {};
      dayGroupsByDateStringByYear[year] = dayGroupsForYear;
    }
    putInDayGroup(occ, dayGroupsForYear);
  }

  function putInDayGroup(occ, dayGroupsForYear) {
    const dateString = new Date(occ.entity.date).toISOString();
    var dayGroup = dayGroupsForYear[dateString];
    if (!dayGroup) {
      dayGroup = { day: dateString, occs: [] };
      dayGroupsForYear[dateString] = dayGroup;
    }
    dayGroup.occs.push(occ);
    dayGroup.occs.sort();
  }
}

// Scales
var yearWidthScale = d3
  .scaleLinear()
  .domain([0, mostOccsInAYear])
  .range([0, maxBarLength]);

// Selections
var docContainerSel = d3.select('.doc-container');
var docFrameSel = d3.select('#doc-frame');
var yearMapContainerSel = d3.select('.year-map-container');
var monthMapContainerSel = d3.select('.month-map-container');
var yearMapToggleSel = d3.select('#year-map-toggle-button');
var monthMapToggleSel = d3.select('#month-map-toggle-button');
var docCloseSel = d3.select('#doc-close-button');
var monthContainer = d3.select('.month-map');
var dayContainer = d3.select('.day-map');
var dayTimeline = dayContainer.select('.timeline-layer');

// Handlers
yearMapToggleSel.on('click', onYearMapToggleClick);
monthMapToggleSel.on('click', onMonthMapToggleClick);
docCloseSel.on('click', onDocCloseClick);

((async function init() {
  try {
    let defaultFetchOpts = { credentials: 'include', mode: 'cors' };
    let res = await fetch(selfURL, defaultFetchOpts);
    let fetchesComplete = false;

    if (res.ok) {
      var authData = await res.json();
      console.log('authData', authData);

      res = await fetch(searchURL, defaultFetchOpts);
      if (res.ok) {
        let searchData = await res.json();
        console.log(searchData);
        fetchesComplete = true;
      }
    }
    if (!fetchesComplete) {
      throw new Error(`Error while authorizing with DocumentCloud: ${error.message}`);
    }
  } catch (error) {
    handleError(error);
  }
})());

function handleError(error) {
  // TODO
  console.error(error);
}

function useOccs(occs) {
  occs.sort(compareOccDates);
  var sortedOccs = populateOccsDict();
  const firstYear = sortedOccs[0];
  dayContainer.attr('height', dayTimelineHeight);
  renderDayTimeline(firstYear);
  renderMonthMap(firstYear);
  renderYearMap(sortedOccs);
}

function renderDayTimeline(year) {
  var dayGroupsByDateString = dayGroupsByDateStringByYear[year];

  var ticks = dayTimeline
    .selectAll('.tick')
    .data(Object.keys(dayGroupsByDateString), getIdForDate);

  ticks.exit().remove();

  var newTicks = ticks.enter().append('g').classed('tick', true);

  newTicks
    .append('line')
    .classed('tick-line', true)
    .attr('x1', 0)
    .attr('x2', 50)
    .attr('y1', 0)
    .attr('y2', 0);
  newTicks
    .append('text')
    .text(
      (dateString) => dayGroupsByDateString[dateString].occs[0].entity.title
    )
    .attr('x', 54)
    .attr('y', '0.3em');
  newTicks
    .append('use')
    .attr('href', '#doc-icon-def')
    .attr('x', 320 - 24 - 10)
    .attr('y', -32 / 2);

  newTicks.on('click', onTickClick);

  newTicks
    .merge(ticks)
    .attr('id', getIdForDate)
    .attr('transform', getTransformForTick);

  d3.select('.doc-lists-layer')
    .selectAll('.date-docs-container')
    .data(Object.keys(dayGroupsByDateString), (day) => day)
    .enter()
    .append('foreignObject')
    .classed('date-docs-container', true)
    .classed('hidden', true)
    .attr('id', (date) => 'doc-list-' + getIdForDate(date))
    .attr('y', getYWithinYearForDate)
    .attr('width', 200)
    .attr('height', 200)
    .append('xhtml:div')
    .append('xhtml:ul')
    .selectAll('li')
    .data((day) => dayGroupsByDateString[day].occs)
    .enter()
    .append('li')
    .text((occ) => occ.document.title)
    .on('click', onDocItemClick);
}

function renderYearMap(sortedOccs) {
  var yearContainer = d3.select('.year-map');

  yearContainer
    .attr('height', sortedOccs.length * yearHeight)
    .attr('width', maxBarLength);

  var newBars = yearContainer
    .select('.timeline-layer')
    .selectAll('.year')
    .data(Object.keys(occsByYear), (x) => x)
    .enter()
    .append('g')
    .classed('year', true);

  newBars
    .append('rect')
    .classed('bar', true)
    .attr('height', yearHeight)
    .attr('width', (year) => yearWidthScale(occsByYear[year].length));
  newBars
    .append('text')
    .text((year) => year)
    .attr('x', 5)
    .attr('y', '1em');
  newBars
    .append('text')
    .text((year) => `${occsByYear[year].length} documents`)
    .attr('x', 5)
    .attr('y', '2em');
  newBars.attr('transform', getTransformForYear);
  newBars.on('click', onYearClick);
}

function renderMonthMap(year) {
  var occsByMonth = groupOccsByMonth(occsByYear[year]);
  var monthWidthScale = d3
    .scaleLinear()
    .domain([
      0,
      Object.values(occsByMonth).reduce(
        (maxOccs, occs) => (occs.length > maxOccs ? occs.length : maxOccs),
        0
      ),
    ])
    .range([0, maxBarLength]);

  monthContainer.attr('height', 12 * monthHeight).attr('width', maxBarLength);

  var months = monthContainer
    .select('.timeline-layer')
    .selectAll('.month')
    .data(Object.keys(occsByMonth), (x) => x);

  months.exit().remove();

  var newMonths = months.enter().append('g').classed('month', true);

  newMonths.append('rect').classed('bar', true).attr('height', monthHeight);
  newMonths
    .append('text')
    .text((month) => englishMonthNames[month])
    .attr('x', 5)
    .attr('y', '1em');
  newMonths
    .append('text')
    .attr('x', 5)
    .attr('y', '2em')
    .classed('doc-count', true);
  newMonths.attr(
    'transform',
    (month) => `translate(0, ${monthHeight * month})`
  );

  var currentMonths = months.merge(newMonths);
  currentMonths
    .select('.bar')
    .attr('width', (month) => monthWidthScale(occsByMonth[month].length));
  currentMonths
    .select('.doc-count')
    .text((month) => `${occsByMonth[month].length} documents`);
  // onMonthClick needs to be rebound on every render so that
  // occsByMonth is correct when the click happens.
  currentMonths.on('click', onMonthClick);

  function onMonthClick(e, month) {
    var sortedOccs = occsByMonth[month];
    if (!sortedOccs || sortedOccs.length < 1) {
      return;
    }

    scrollOccurrenceIntoView(sortedOccs[0]);
  }
}

function getTransformForTick(dateString) {
  return `translate(0, ${getYWithinYearForDate(dateString)})`;
}

function getYWithinYearForDate(dateString) {
  const date = new Date(dateString);
  const startOfYear = new Date(date.getFullYear(), 0, 1);
  const daysFromStartOfYear =
    (date.getTime() - startOfYear.getTime()) / (1000 * 60 * 60 * 24);
  // The added 0.5 is to keep the first tick from being halfway cut off.
  return (daysFromStartOfYear + 0.5) * dayHeight;
}

function getTransformForYear(year, i) {
  const y = i * yearHeight;
  return `translate(0, ${y})`;
}

function onDocItemClick(e, occ) {
  docFrameSel.attr(
    'src',
    `https://embed.documentcloud.org/documents/${occ.document.id}/?embed=1&amp;responsive=1&amp;title=1`
  );
  docContainerSel.attr('title', occ.document.title);
  docContainerSel.select('.excerpt').text(occ.excerpt);
  docContainerSel.classed('hidden', false);
}

function onTickClick(e, day) {
  d3.selectAll('.date-docs-container').classed('hidden', true);
  d3.select(`#doc-list-${getIdForDate(day)}`).classed('hidden', false);
}

function onYearClick(e, year) {
  var sortedOccs = occsByYear[year];
  if (!sortedOccs || sortedOccs.length < 1) {
    return;
  }

  renderMonthMap(year);
  renderDayTimeline(year);
  scrollOccurrenceIntoView(sortedOccs[0]);
}

function onYearMapToggleClick() {
  yearMapContainerSel.classed('hidden', !yearMapContainerSel.classed('hidden'));
  yearMapToggleSel.text(
    yearMapContainerSel.classed('hidden') ? 'Show year map' : 'Hide year map'
  );
}

function onMonthMapToggleClick() {
  monthMapContainerSel.classed(
    'hidden',
    !monthMapContainerSel.classed('hidden')
  );
  monthMapToggleSel.text(
    monthMapContainerSel.classed('hidden') ? 'Show month map' : 'Hide month map'
  );
}

function onDocCloseClick() {
  docContainerSel.classed('hidden', true);
}

function scrollOccurrenceIntoView(occ) {
  var textSel = d3.select(`#${getIdForDate(occ.entity.date)} text`);
  textSel.node().scrollIntoView({ behavior: 'smooth' });
}

function groupOccsByMonth(occs) {
  var occsByMonth = {};
  occs.forEach(putInMonthDict);
  return occsByMonth;

  function putInMonthDict(occ) {
    const month = new Date(occ.entity.date).getMonth();
    var occsForMonth = occsByMonth[month];
    if (!occsForMonth) {
      occsForMonth = [];
      occsByMonth[month] = occsForMonth;
    }
    occsForMonth.push(occ);
    occsForMonth.sort((a, b) => (a.entity.date < b.entity.date ? -1 : 1));
  }
}

function getIdForDate(dateString) {
  return 'docs-container-' + dateString.slice(0, 10);
}

function compareOccDates(a, b) {
  return new Date(a.entity.date) < new Date(b.entity.date) ? -1 : 1;
}
