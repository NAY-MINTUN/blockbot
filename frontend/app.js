const toolbox = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'category', name: 'Robot', colour: '210',
      contents: [
        { kind: 'block', type: 'when_run' },
        { kind: 'block', type: 'move_joint' },
        { kind: 'block', type: 'wait' }
      ]
    },
    {
      kind: 'category', name: 'Logic', colour: '210',
      contents: [
        { kind: 'block', type: 'controls_if' },
        { kind: 'block', type: 'logic_compare' },
        { kind: 'block', type: 'logic_operation' },
        { kind: 'block', type: 'logic_boolean' }
      ]
    },
    {
      kind: 'category', name: 'Loops', colour: '120',
      contents: [
        { kind: 'block', type: 'controls_repeat_ext' },
        { kind: 'block', type: 'controls_whileUntil' }
      ]
    },
    {
      kind: 'category', name: 'Math', colour: '230',
      contents: [
        { kind: 'block', type: 'math_number' },
        { kind: 'block', type: 'math_arithmetic' }
      ]
    },
    { kind: 'category', name: 'Variables', colour: '330', custom: 'VARIABLE' },
    { kind: 'category', name: 'Functions', colour: '290', custom: 'PROCEDURE' }
  ]
};

const BACKEND = 'ws://127.0.0.1:8000/ws';

let socket;

function setStatus(connected) {
  document.getElementById('status').style.background =
    connected ? '#2ecc71' : '#c0392b';

}

function connect() {
  socket = new WebSocket(BACKEND);
  socket.onopen = () => setStatus(true);
  socket.onclose = () => { setStatus(false); setTimeout(connect, 1000); };
  socket.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (!msg.ok) {
      console.warn('Command failed:', msg.error);
      document.getElementById('status').title = msg.error;
    }
  };
}
connect();
function send(message) {
  if (socket && socket.readyState === WebSocket.OPEN)
    socket.send(JSON.stringify(message));
}

function moveJoint(channel, angle) { send({ cmd: 'move', channel, angle }); }
function wait(seconds) { send({ cmd: 'wait', second: seconds }); }

const workspace = Blockly.inject('workspace', {
  toolbox,
  renderer: 'zelos',
  trashcan: true,
  zoom: { controls: true, wheel: true, startScale: 0.9, minScale: 0.5, maxScale: 2 },
  move: { scrollbars: true, drag: true, wheel: false },
  grid: { spacing: 24, length: 3, colour: '#eee', snap: true }
});

function saveProgram() {
  localStorage.setItem('blockbot',
    JSON.stringify(Blockly.serialization.workspaces.save(workspace)));
}

function loadProgram() {
  const saved = localStorage.getItem('blockbot');
  if (saved)
    Blockly.serialization.workspaces.load(JSON.parse(saved), workspace);
}

loadProgram();
workspace.addChangeListener(saveProgram);

document.getElementById('run').addEventListener('click', () => {
  const code = javascript.javascriptGenerator.workspaceToCode(workspace);
  new Function('moveJoint', 'wait', code)(moveJoint, wait);
});