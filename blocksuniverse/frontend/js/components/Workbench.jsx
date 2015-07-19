'use strict';

import React from 'react';
import component from '../util/component.js';

import Block from './Block.jsx';

const Workbench = component('Workbench', function() {
  return (
    <div>
      <Block/>
    </div>
  );
});

export default Workbench;
