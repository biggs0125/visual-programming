'use strict';

import React from 'react';
import component from '../util/component.js';

const InputSlot = component('InputSlot', function({type}) {
  return (
    <div className={`slot--${type} input-slot`}>
      <div className='slot-snap-helper'></div>
      <div className='input-slot-wall left-wall'></div>
      <div className='input-slot-wall right-wall'></div>
    </div>
  );
});

export default InputSlot;
