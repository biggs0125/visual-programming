'use strict';

import React from 'react';
import component from '../util/component.js';

import Block from './Block.jsx';

const WorkbenchHelpers = {
}

const Workbench = component('Workbench', WorkbenchHelpers, function({inputLocations}) {
  return (
    <div>
      <Block inputTypes={['INT', 'STRING', 'BOOL', 'STRING', 'INT']} outputType='INT'inputLocations={inputLocations}/>
      <Block inputTypes={['INT', 'INT', 'BOOL', 'INT']} outputType='STRING' inputLocations={inputLocations}/>  
    </div>
  );
});

export default Workbench;
