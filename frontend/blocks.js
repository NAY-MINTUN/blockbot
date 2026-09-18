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

// Blockly's built-in procedure generators create synchronous JavaScript
// functions. BlockBot commands are asynchronous, so procedures must be async
// as well; otherwise a procedure would finish before its robot movements do.
function procedureArguments(block, generator) {
  return block.getVars().map(argument => generator.nameDB_.getName(
    argument,
    Blockly.Names.NameType.VARIABLE,
  ));
}

gen.forBlock.procedures_defnoreturn = (block, generator) => {
  const name = generator.getProcedureName(block.getFieldValue('NAME'));
  const argumentsList = procedureArguments(block, generator);
  const body = generator.statementToCode(block, 'STACK');
  generator.definitions_[`%${name}`] =
    `async function ${name}(${argumentsList.join(', ')}) {\n${body}}\n`;
  return null;
};

gen.forBlock.procedures_defreturn = (block, generator) => {
  const name = generator.getProcedureName(block.getFieldValue('NAME'));
  const argumentsList = procedureArguments(block, generator);
  const body = generator.statementToCode(block, 'STACK');
  const returnValue = generator.valueToCode(block, 'RETURN', javascript.Order.NONE) || 'null';
  generator.definitions_[`%${name}`] =
    `async function ${name}(${argumentsList.join(', ')}) {\n${body}  return ${returnValue};\n}\n`;
  return null;
};

gen.forBlock.procedures_callnoreturn = (block, generator) => {
  const name = generator.getProcedureName(block.getFieldValue('NAME'));
  const argumentsList = Array.from({ length: block.argumentCount_ }, (_, index) =>
    generator.valueToCode(block, `ARG${index}`, javascript.Order.NONE) || 'null');
  return `await ${name}(${argumentsList.join(', ')});\n`;
};

gen.forBlock.procedures_callreturn = (block, generator) => {
  const name = generator.getProcedureName(block.getFieldValue('NAME'));
  const argumentsList = Array.from({ length: block.argumentCount_ }, (_, index) =>
    generator.valueToCode(block, `ARG${index}`, javascript.Order.NONE) || 'null');
  return [`await ${name}(${argumentsList.join(', ')})`, javascript.Order.AWAIT];
};
