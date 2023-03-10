// > new Date(d.getTime() + 1000 * 60 * 60 * 24 * -1000).getTime()
const baseDateTime = 1591654756074;
const dayInMS = 1000 * 60 * 60 * 24;

var words = [
  'cat',
  'dog',
  'potato',
  'crime',
  'report',
  'culture',
  'election',
  'robot'
];

function makeTitle(n) {
  return words[n % words.length] + ' ' + words[(n + (n % 5)) % words.length];
}

function range(n) {
  var array = [];
  for (let i = 0; i < n; ++i) {
    array.push(i);
  }
  return array;
}

var lastDateTime = baseDateTime;

function entityOccurrenceForN(n) {
  const step = (n % 5);
  lastDateTime += step * dayInMS;
  var lastDate = new Date(lastDateTime);
  return {
    entity: {
      id: n,
      title: lastDate.toDateString(),
      date: lastDate
    },
    document: {
      id: n + 1000000,
      title: makeTitle(n),
      url: 'https://hey.what'
    }
  };
}

console.log(JSON.stringify(range(150).map(entityOccurrenceForN), null, 2));
