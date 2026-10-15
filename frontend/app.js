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
const jointNames = ['Base','In / Out','Up / Down','Gripper'];
let devices = [];
let activeDevice = null;
let authMode = 'login';
let accountToken = null;
let programSaveTimer;

const statusElement = document.getElementById('status');
const statusText = document.getElementById('statusText');
const emergencyStopButton = document.getElementById('emergencyStop');
const runButton = document.getElementById('run');
const newButton = document.getElementById('newProgram');
const toast = document.getElementById('toast');
const servoPositionElements = [0, 1, 2, 3]
  .map(channel => document.getElementById(`servoPosition${channel}`));

let socket;
let reconnectTimer;
let reconnectAttempt = 0;
let toastTimer;
let emergencyStopResetTimer;
let running = false;
let stopRequested = false;
let pendingReply;

function showToast(message, isError = false) {
  if (activeDevice?.type !== 'robot-arm') {
    toast.classList.remove('toast--visible');
    return;
  }
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
  runButton.disabled = state !== 'connected' || running || stopRequested;
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
  if (!accountToken || !activeDevice || activeDevice.type !== 'robot-arm' || !hasValidLimits(activeDevice)) return;
  window.clearTimeout(reconnectTimer);
  if (socket && socket.readyState < WebSocket.CLOSING) {
    socket.onclose = null;
    socket.close();
  }
  setStatus(reconnectAttempt === 0 ? 'connecting' : 'offline', 'Trying to reconnect…');
  const params = new URLSearchParams();
  params.set('device', activeDevice.address);
  params.set('token', accountToken);
  params.set('limits', JSON.stringify(activeDevice.limits));
  const target = params.size ? `?${params}` : '';
  const connection = new WebSocket(`${backendUrl}${target}`);
  socket = connection;

  connection.onopen = () => {
    if (socket !== connection) return;
    setStatus('connecting', 'Checking the robot connection…');
  };

  connection.onclose = () => {
    if (socket !== connection) return;
    if (pendingReply) {
      pendingReply.reject(new Error('The robot disconnected.'));
      pendingReply = null;
    }
    setStatus('offline', 'Trying to reconnect…');
    const delay = Math.min(1000 * (2 ** reconnectAttempt), 8000);
    reconnectAttempt += 1;
    reconnectTimer = window.setTimeout(connect, delay);
  };

  connection.onerror = () => connection.close();

  connection.onmessage = (event) => {
    if (socket !== connection) return;
    let message;
    try {
      message = JSON.parse(event.data);
    } catch {
      return;
    }

    if (message.type === 'positions') {
      if (!Array.isArray(message.angles) || message.angles.some(angle => typeof angle !== 'number')) return;
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

function saveDevices() {
  document.getElementById('deviceCount').textContent = devices.length;
  renderDevices();
  saveAccountState();
}
function hasValidLimits(device) {
  return Array.isArray(device?.limits) && device.limits.length === 4 && device.limits.every(item => item && item.min !== '' && item.max !== '' && item.min !== null && item.max !== null && Number.isFinite(Number(item.min)) && Number.isFinite(Number(item.max)) && Number(item.min) < Number(item.max));
}
function renderDevices() {
  const list = document.getElementById('deviceList');
  list.replaceChildren();
  devices.forEach(device => {
    const card = document.createElement('section'); card.className='device-card';
    const limits = device.limits || Array.from({length:4},()=>({min:'',max:''}));
    card.innerHTML = `<div class="device-card__top"><div><h3></h3><p></p></div><div class="device-card__actions"><button type="button" class="button button--secondary device-card__connect">${activeDevice?.id===device.id?'Selected':'Connect'}</button><button type="button" class="button button--delete device-card__delete">Delete</button></div></div>`;
    card.querySelector('h3').textContent=device.name;
    card.querySelector('p').textContent=`${device.type==='robot-arm'?'Robot arm':'Other device'} · ${device.address}`;
    card.querySelector('.device-card__connect').addEventListener('click',()=>{ if(activeDevice?.id!==device.id&&socket&&socket.readyState<WebSocket.CLOSING){socket.onclose=null;socket.close();} activeDevice=device; applyDeviceVisibility(); if(device.type==='robot-arm'){if(!hasValidLimits(device)){setStatus('offline','Enter all four joint ranges to connect.');showToast('Enter the minimum and maximum for all four joints before connecting.',true);return;} connect();} else { setStatus('offline','This device type does not have a BlockBot driver yet.');} renderDevices(); document.getElementById('devicesDialog').close(); });
    card.querySelector('.device-card__delete').setAttribute('aria-label',`Delete ${device.name}`);
    card.querySelector('.device-card__delete').addEventListener('click',()=>{
      if(!window.confirm(`Delete ${device.name} from your devices?`))return;
      const deletingActiveDevice=activeDevice?.id===device.id;
      devices=devices.filter(item=>item.id!==device.id);
      if(deletingActiveDevice){
        window.clearTimeout(reconnectTimer);
        if(socket){socket.onclose=null;socket.close();socket=null;}
        if(pendingReply){pendingReply.reject(new Error('The selected device was deleted.'));pendingReply=null;}
        activeDevice=null;
      }
      saveDevices();
      if(deletingActiveDevice)applyDeviceVisibility();
    });
    if (device.type==='robot-arm') {
      const grid=document.createElement('div'); grid.className='limit-grid';
      limits.forEach((range,index)=>{
        const label=document.createElement('label');
        label.textContent=`${jointNames[index]} minimum and maximum (degrees)`;
        const row=document.createElement('div'); row.style.display='flex'; row.style.gap='6px';
        ['min','max'].forEach(bound=>{ const input=document.createElement('input'); input.type='number'; input.min='0'; input.max='180'; input.placeholder=bound==='min'?'Min°':'Max°'; input.value=range[bound] ?? ''; input.setAttribute('aria-label',`${jointNames[index]} ${bound}`); input.addEventListener('change',()=>{ const min=Number(row.children[0].value), max=Number(row.children[1].value); if(!row.children[0].value||!row.children[1].value||min<0||max>180||min>=max){showToast('Enter both joint limits from 0° to 180°, with minimum lower than maximum.',true);return;} range.min=min;range.max=max;saveDevices();if(activeDevice?.id===device.id){applyBlocklyAngleLimits();connect();} }); row.append(input); });
        label.append(row);grid.append(label);
      }); card.append(grid);
    }
    list.append(card);
  });
}
document.getElementById('devicesButton').addEventListener('click',()=>{renderDevices();document.getElementById('devicesDialog').showModal();});
document.getElementById('emptyAddDevice').addEventListener('click',()=>document.getElementById('devicesDialog').showModal());
document.getElementById('addDeviceForm').addEventListener('submit',event=>{event.preventDefault();const form=new FormData(event.currentTarget);const address=String(form.get('address')).trim();if(!/^wss?:\/\//i.test(address)){document.getElementById('discoveredDevices').textContent='Enter a WebSocket address, or use Find devices after Wi‑Fi setup.';return;}const type=form.get('type');const device={id:crypto.randomUUID(),name:String(form.get('name')).trim(),type,address,limits:Array.from({length:4},()=>({min:'',max:''}))};devices.push(device);activeDevice=device;saveDevices();applyDeviceVisibility();event.currentTarget.reset();document.getElementById('deviceList').scrollIntoView();});
document.getElementById('discoverDevices').addEventListener('click',async()=>{const region=document.getElementById('discoveredDevices');region.textContent='Looking for BlockBot devices…';try{const response=await fetch(`/api/devices/discover?token=${encodeURIComponent(accountToken)}`);const result=await response.json();if(!response.ok)throw new Error(result.detail||'Discovery failed.');region.replaceChildren();if(!result.devices.length){region.textContent=result.available?'No BlockBot arms found. Check that this computer and the arm are on the same Wi‑Fi.':'Discovery is unavailable on this server.';return;}result.devices.forEach(found=>{const button=document.createElement('button');button.className='button button--secondary';button.textContent=`Add ${found.name}`;button.onclick=()=>{const device={id:crypto.randomUUID(),name:found.name,type:'robot-arm',address:found.address,limits:Array.from({length:4},()=>({min:'',max:''}))};devices.push(device);activeDevice=device;saveDevices();applyDeviceVisibility();region.replaceChildren();};region.append(button);});}catch(error){region.textContent=error.message;}});

function applyDeviceVisibility(){
  const selectedRobot=activeDevice?.type==='robot-arm';
  document.getElementById('noRobotState').hidden=selectedRobot;
  document.getElementById('workspace').style.visibility=selectedRobot?'visible':'hidden';
  document.getElementById('coach').hidden=!selectedRobot;
  document.querySelector('.servo-monitor').hidden=!selectedRobot;
  document.getElementById('run').hidden=!selectedRobot;
  document.getElementById('emergencyStop').hidden=!selectedRobot;
  document.getElementById('newProgram').hidden=!selectedRobot;
  if(selectedRobot){workspace.updateToolbox(toolbox);if(workspace.getAllBlocks(false).length===0)createStarterProgram();applyBlocklyAngleLimits();Blockly.svgResize(workspace);}
  else workspace.updateToolbox({kind:'categoryToolbox',contents:[]});
  if(!selectedRobot)setStatus('offline','Add or select a robot arm to connect.');
}

function applyBlocklyAngleLimits(){
  if(activeDevice?.type!=='robot-arm'||!hasValidLimits(activeDevice))return;
  workspace.getAllBlocks(false).filter(block=>block.type==='move_joint').forEach(block=>{
    const joint=Number(block.getFieldValue('JOINT'));
    const range=activeDevice.limits[joint];
    const field=block.getField('ANGLE');
    if(!field)return;
    const low=Number(range.min),high=Number(range.max);
    field.setConstraints(low,high,null);
    const current=Number(block.getFieldValue('ANGLE'));
    if(current<low)field.setValue(low);
    else if(current>high)field.setValue(high);
  });
}

async function saveAccountState(){
  if(!accountToken)return;
  window.clearTimeout(programSaveTimer);
  const state={devices,program:Blockly.serialization.workspaces.save(workspace)};
  document.getElementById('saveState').textContent='Saving…';
  programSaveTimer=window.setTimeout(()=>fetch(`/api/state?token=${encodeURIComponent(accountToken)}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(state)}).then(response=>{if(!response.ok)throw new Error('Save failed');document.getElementById('saveState').textContent='Saved';}).catch(()=>{document.getElementById('saveState').textContent='Save failed';}),350);
}

function setAuthenticated(){document.getElementById('authGate').hidden=true;document.getElementById('appShell').classList.add('is-authenticated');document.getElementById('deviceCount').textContent=devices.length;applyDeviceVisibility();}
async function restoreAccount(){if(!accountToken)return;try{const response=await fetch(`/api/state?token=${encodeURIComponent(accountToken)}`);if(!response.ok)throw new Error();const state=await response.json();devices=Array.isArray(state.devices)?state.devices:[];const saved=state.program;if(saved)Blockly.serialization.workspaces.load(saved,workspace);else workspace.clear();activeDevice=devices.find(item=>item.type==='robot-arm')||devices[0]||null;setAuthenticated();if(activeDevice?.type==='robot-arm'&&hasValidLimits(activeDevice))connect();}catch{accountToken=null;localStorage.removeItem('blockbot.token');}}

document.getElementById('authModeButton').addEventListener('click',()=>{authMode=authMode==='login'?'signup':'login';document.getElementById('authHeading').textContent=authMode==='login'?'Sign in':'Create account';document.querySelector('#authPageForm button[type=submit]').textContent=authMode==='login'?'Sign in':'Create account';document.getElementById('authModeButton').textContent=authMode==='login'?'Create an account':'I already have an account';document.getElementById('authError').textContent='';});
document.getElementById('togglePassword').addEventListener('click',event=>{
  const password=document.getElementById('authPassword');
  const visible=password.type==='password';
  password.type=visible?'text':'password';
  event.currentTarget.setAttribute('aria-pressed',String(visible));
  event.currentTarget.setAttribute('aria-label',visible?'Hide password':'Show password');
  document.getElementById('passwordEyeSlash').hidden=!visible;
});
document.getElementById('authPageForm').addEventListener('submit',async event=>{event.preventDefault();const form=new FormData(event.currentTarget);try{const response=await fetch(`/api/auth/${authMode}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:form.get('email'),password:form.get('password')})});const data=await response.json();if(!response.ok)throw new Error(data.detail||'Account request failed.');accountToken=data.token;localStorage.setItem('blockbot.token',accountToken);const stateResponse=await fetch(`/api/state?token=${encodeURIComponent(accountToken)}`);const state=await stateResponse.json();devices=state.devices||[];if(state.program)Blockly.serialization.workspaces.load(state.program,workspace);activeDevice=devices.find(item=>item.type==='robot-arm')||devices[0]||null;setAuthenticated();if(activeDevice?.type==='robot-arm'&&hasValidLimits(activeDevice))connect();}catch(error){document.getElementById('authError').textContent=error.message;}});
document.getElementById('accountButton').addEventListener('click',async()=>{if(accountToken)await fetch('/api/auth/logout',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({token:accountToken})});window.clearTimeout(reconnectTimer);window.clearTimeout(programSaveTimer);accountToken=null;localStorage.removeItem('blockbot.token');devices=[];activeDevice=null;if(socket){socket.onclose=null;socket.close();}document.getElementById('appShell').classList.remove('is-authenticated');document.getElementById('authGate').hidden=false;workspace.clear();});
document.getElementById('deviceCount').textContent='0';
accountToken=localStorage.getItem('blockbot.token');
restoreAccount();

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
  if (stopRequested) {
    return Promise.reject(new Error('Program stopped by emergency stop.'));
  }
  return sendCommand({ cmd: 'move', channel, angle });
}

function wait(seconds) {
  return new Promise(resolve => window.setTimeout(resolve, seconds * 1000));
}

const workspace = Blockly.inject('workspace', {
  toolbox: {kind:'categoryToolbox',contents:[]},
  renderer: 'zelos',
  trashcan: true,
  sounds: false,
  zoom: { controls: true, wheel: true, startScale: 0.92, minScale: 0.5, maxScale: 2 },
  move: { scrollbars: true, drag: true, wheel: false },
  grid: { spacing: 24, length: 3, colour: '#DCE7F2', snap: true }
});

function saveProgram() {
  saveAccountState();
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

function generateProgramCode(startBlocks) {
  const generator = javascript.javascriptGenerator;
  generator.init(workspace);

  // Procedure definitions are separate top-level blocks, not children of the
  // Run block. Generate them first so calls made by the Run program exist.
  workspace.getTopBlocks(true)
    .filter(block => block.type === 'procedures_defnoreturn' || block.type === 'procedures_defreturn')
    .forEach(block => generator.blockToCode(block));

  const statements = startBlocks
    .map(block => block.getNextBlock())
    .filter(Boolean)
    .map(block => generator.blockToCode(block))
    .map(result => Array.isArray(result) ? result[0] : result)
    .join('\n');

  return generator.finish(statements);
}

workspace.addChangeListener(event => {
  if (!event.isUiEvent) {
    applyBlocklyAngleLimits();
    saveProgram();
  }
});

async function emergencyStop() {
  window.clearTimeout(emergencyStopResetTimer);
  stopRequested = true;
  running = false; // prevents more Blockly commands from being sent

  try {
    await sendCommand({ cmd: 'estop' });
    showToast('Emergency stop activated. It will reset automatically in 5 seconds.', true);
    emergencyStopResetTimer = window.setTimeout(() => {
      emergencyStopResetTimer = undefined;
      resetEmergencyStop();
    }, 5000);
  } catch (error) {
    showToast(`Stop command failed: ${error.message}`, true);
  }

  runButton.classList.remove('button--running');
  document.getElementById('runText').textContent = 'Run';
  setStatus(socket?.readyState === WebSocket.OPEN ? 'connected' : 'offline');
}

emergencyStopButton.addEventListener('click', emergencyStop);

async function resetEmergencyStop() {
  window.clearTimeout(emergencyStopResetTimer);
  emergencyStopResetTimer = undefined;

  try {
    await sendCommand({ cmd: 'reset_estop' });
    stopRequested = false;
    setStatus(socket?.readyState === WebSocket.OPEN ? 'connected' : 'offline');
    showToast('Emergency stop reset automatically. Robot controls are ready.');
  } catch (error) {
    showToast(`Could not reset stop: ${error.message}`, true);
  }
}

newButton.addEventListener('click', () => {
  if (!window.confirm('Start a new program? Your current blocks will be cleared.')) return;
  workspace.clear();
  createStarterProgram();
  saveProgram();
  showToast('New program ready.');
});

runButton.addEventListener('click', async () => {
  if (stopRequested) {
    showToast('Reset the emergency stop before running a new program.', true);
    return;
  }

  const startBlocks = workspace.getTopBlocks(true).filter(block => block.type === 'when_run');
  if (startBlocks.length === 0) {
    showToast('Add a “when Run clicked” block first.', true);
    return;
  }

  const code = generateProgramCode(startBlocks);

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
  window.clearTimeout(emergencyStopResetTimer);
  socket?.close();
});
