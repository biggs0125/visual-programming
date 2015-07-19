'use strict';

import React from 'react';
import component from '../util/component.js';

const OutputSlot = component('OutputSlot', function({type}) {
  return (
    <div className={`slot--${type} output-slot`}>
      <div className='output-slot-wall left-wall'></div>
      <div className='output-slot-wall right-wall'></div>
    </div>
  );
});

export default OutputSlot;
