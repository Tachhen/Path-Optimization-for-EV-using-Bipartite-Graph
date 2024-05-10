var assert = require('assert');

var twoColorGraph = function (N, d) {
  //your code here
};

try {
  N = 4;
  dislikes = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
  ];
  assert.equal(twoColorGraph(N, dislikes), true);

  console.log('PASSED: ' + 'First Test');
} catch (err) {
  console.log(err);
}

try {
  N = 4;
  dislikes = [
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
  ];
  assert.equal(twoColorGraph(N, dislikes), true);

  console.log('PASSED: ' + 'Second Test');
} catch (err) {
  console.log(err);
}

try {
  N = 4;
  dislikes = [
    [1, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
  ];
  assert.equal(twoColorGraph(N, dislikes), false);

  console.log('PASSED: ' + 'Third Test');
} catch (err) {
  console.log(err);
}
