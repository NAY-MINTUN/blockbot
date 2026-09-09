const toolbox = {
  kind: 'categoryToolbox',
  contents: [
    {
      kind: 'category', name: 'Robot', colour: '#007EE9',
      contents: [
        { kind: 'block', type: 'when_run' },
        { kind: 'block', type: 'move_joint' },
        { kind: 'block', type: 'wait' }
      ]
    },
    {
      kind: 'category', name: 'Logic', colour: '#5B6ABF',
      contents: [
        { kind: 'block', type: 'controls_if' },
        { kind: 'block', type: 'logic_compare' },
        { kind: 'block', type: 'logic_operation' },
        { kind: 'block', type: 'logic_boolean' }
      ]
    },
    {
      kind: 'category', name: 'Loops', colour: '#2F9E6F',
      contents: [
        { kind: 'block', type: 'controls_repeat_ext' },
        { kind: 'block', type: 'controls_whileUntil' }
      ]
    },
    {
      kind: 'category', name: 'Math', colour: '#6574C4',
      contents: [
        { kind: 'block', type: 'math_number' },
        { kind: 'block', type: 'math_arithmetic' }
      ]
    },
    { kind: 'category', name: 'Variables', colour: '#B05B78', custom: 'VARIABLE' },
    { kind: 'category', name: 'Functions', colour: '#8D5BB5', custom: 'PROCEDURE' }
  ]
};

const backendUrl = (() => {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const isStandaloneDevServer = location.port === '5500';
  const host = isStandaloneDevServer ? `${location.hostname}:8000` : location.host;
  return `${protocol}//${host}/ws`;
})();

const statusElement = document.getElementById('status');
const statusText = document.getElementById('statusText');
const runButton = document.getElementById('run');
const newButton = document.getElementById('newProgram');
const toast = document.getElementById('toast');
const servoPositionElements = [0, 1, 2, 3]
  .map(channel => document.getElementById(`servoPosition${channel}`));

let socket;
let reconnectTimer;
let reconnectAttempt = 0;
let toastTimer;
let running = false;
let pendingReply;

function showToast(message, isError = false) {
  window.clearTimeout(toastTimer);
  toast.textContent = message;
  toast.classList.toggle('toast--error', isError);
  toast.classList.add('toast--visible');
  toastTimer = window.setTimeout(() => toast.classList.remove('toast--visible'), 3200);
}

function setStatus(state, detail = '') {
  const labels = {
    connecting: 'Connecting…',
    connected: 'Robot connected',
    offline: 'Robot offline'
  };

  statusElement.className = `connection-status connection-status--${state}`;
  statusText.textContent = labels[state];
  statusElement.title = detail || labels[state];
  runButton.disabled = state !== 'connected' || running;
}

function updateServoPositions(angles) {
  if (!Array.isArray(angles) || angles.length !== servoPositionElements.length) return;
  angles.forEach((angle, channel) => {
    if (typeof angle === 'number') {
      servoPositionElements[channel].textContent = `${Math.round(angle)}°`;
    }
  });
}

function connect() {
  window.clearTimeout(reconnectTimer);
  setStatus(reconnectAttempt === 0 ? 'connecting' : 'offline', 'Trying to reconnect…');
  socket = new WebSocket(backendUrl);

  socket.onopen = () => {
    setStatus('connecting', 'Checking the robot connection…');
  };

  socket.onclose = () => {
    if (pendingReply) {
      pendingReply.reject(new Error('The robot disconnected.'));
      pendingReply = null;
    }
    setStatus('offline', 'Trying to reconnect…');
    const delay = Math.min(1000 * (2 ** reconnectAttempt), 8000);
    reconnectAttempt += 1;
    reconnectTimer = window.setTimeout(connect, delay);
  };

  socket.onerror = () => socket.close();

  socket.onmessage = (event) => {
    let message;
    try {
      message = JSON.parse(event.data);
    } catch {
      return;
    }

    if (message.type === 'positions') {
      reconnectAttempt = 0;
      setStatus('connected');
      updateServoPositions(message.angles);
      return;
    }

    if (pendingReply) {
      const { resolve, reject } = pendingReply;
      pendingReply = null;
      message.ok ? resolve(message) : reject(new Error(message.error || 'Command failed.'));
    } else if (!message.ok) {
      showToast(message.error || 'The robot is unavailable.', true);
      statusElement.title = message.error || 'The robot is unavailable.';
    }
  };
}

function sendCommand(message) {
  return new Promise((resolve, reject) => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      reject(new Error('Connect to the robot before running your program.'));
      return;
    }
    if (pendingReply) {
      reject(new Error('The previous robot command is still running.'));
      return;
    }
    pendingReply = { resolve, reject };
    socket.send(JSON.stringify(message));
  });
}

function moveJoint(channel, angle) {
  return sendCommand({ cmd: 'move', channel, angle });
}

function wait(seconds) {
  return new Promise(resolve => window.setTimeout(resolve, seconds * 1000));
}

const workspace = Blockly.inject('workspace', {
  toolbox,
  renderer: 'zelos',
  trashcan: true,
  sounds: false,
  zoom: { controls: true, wheel: true, startScale: 0.92, minScale: 0.5, maxScale: 2 },
  move: { scrollbars: true, drag: true, wheel: false },
  grid: { spacing: 24, length: 3, colour: '#DCE7F2', snap: true }
});

function saveProgram() {
  localStorage.setItem('blockbot', JSON.stringify(Blockly.serialization.workspaces.save(workspace)));
  document.getElementById('saveState').textContent = 'Saved';
}

function createStarterProgram() {
  const start = workspace.newBlock('when_run');
  const move = workspace.newBlock('move_joint');
  start.initSvg();
  move.initSvg();
  start.nextConnection.connect(move.previousConnection);
  start.moveBy(70, 70);
  start.render();
  move.render();
}

function loadProgram() {
  const saved = localStorage.getItem('blockbot');
  if (!saved) {
    createStarterProgram();
    return;
  }
  try {
    Blockly.serialization.workspaces.load(JSON.parse(saved), workspace);
    if (workspace.getAllBlocks(false).length === 0) createStarterProgram();
  } catch {
    localStorage.removeItem('blockbot');
    createStarterProgram();
    showToast('The saved program was reset because it could not be loaded.', true);
  }
}

loadProgram();
workspace.addChangeListener(event => {
  if (!event.isUiEvent) saveProgram();
});

newButton.addEventListener('click', () => {
  if (!window.confirm('Start a new program? Your current blocks will be cleared.')) return;
  workspace.clear();
  createStarterProgram();
  saveProgram();
  showToast('New program ready.');
});

runButton.addEventListener('click', async () => {
  const startBlocks = workspace.getTopBlocks(true).filter(block => block.type === 'when_run');
  if (startBlocks.length === 0) {
    showToast('Add a “when Run clicked” block first.', true);
    return;
  }

  const generator = javascript.javascriptGenerator;
  generator.init(workspace);
  const generatedStatements = startBlocks
    .map(block => block.getNextBlock())
    .filter(Boolean)
    .map(block => generator.blockToCode(block))
    .map(result => Array.isArray(result) ? result[0] : result)
    .join('\n');
  const code = generator.finish(generatedStatements);

  if (!code.trim()) {
    showToast('Snap a robot block under “when Run clicked”.', true);
    return;
  }

  running = true;
  runButton.disabled = true;
  runButton.classList.add('button--running');
  document.getElementById('runText').textContent = 'Running…';

  try {
    const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;
    await new AsyncFunction('moveJoint', 'wait', code)(moveJoint, wait);
    showToast('Program finished!');
  } catch (error) {
    showToast(error.message || 'The program stopped.', true);
  } finally {
    running = false;
    runButton.classList.remove('button--running');
    document.getElementById('runText').textContent = 'Run';
    setStatus(socket?.readyState === WebSocket.OPEN ? 'connected' : 'offline');
  }
});

document.getElementById('coachClose').addEventListener('click', () => {
  document.getElementById('coach').classList.add('coach--hidden');
});

window.addEventListener('beforeunload', () => {
  window.clearTimeout(reconnectTimer);
  socket?.close();
});

connect();
