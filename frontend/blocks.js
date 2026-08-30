Blockly.defineBlocksWithJsonArray([
  {
    type: 'when_run',
    message0: 'when Run clicked',
    nextStatement: null,
    colour: '#E96B00',
    tooltip: 'The program starts with this block.'
  },
  {
    type: 'move_joint',
    message0: 'move %1 to %2 degrees',
    args0: [
      {
        type: 'field_dropdown',
        name: 'JOINT',
        options: [['base', '0'], ['in / out', '1'], ['up / down', '2'], ['gripper', '3']]
      },
      { type: 'field_number', name: 'ANGLE', value: 90, min: 0, max: 180 }
    ],
    previousStatement: null,
    nextStatement: null,
    colour: '#007EE9',
    tooltip: 'Move one robot joint. The backend checks every angle for safety.'
  },
  {
    type: 'wait',
    message0: 'wait %1 seconds',
    args0: [{ type: 'field_number', name: 'SECONDS', value: 1, min: 0, max: 10 }],
    previousStatement: null,
    nextStatement: null,
    colour: '#2F9E6F',
    tooltip: 'Pause before the next block runs.'
  }
]);

const gen = javascript.javascriptGenerator;

gen.forBlock.when_run = () => '';
gen.forBlock.move_joint = block =>
  `await moveJoint(${block.getFieldValue('JOINT')}, ${block.getFieldValue('ANGLE')});\n`;
gen.forBlock.wait = block =>
  `await wait(${block.getFieldValue('SECONDS')});\n`;
