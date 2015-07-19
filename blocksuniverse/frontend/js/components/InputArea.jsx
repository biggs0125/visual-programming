'use strict';

import React from 'react';
import component from '../util/component.js';

import InputSlot from './InputSlot.jsx';

const InputArea = component('InputArea', function({types}) {
  let counter = 0;
  const typemap = types.map((type) => {
    counter++;
    return <InputSlot key={counter} type={type}/>
  });
  return (
    <div className='input-area'>
      {typemap}
    </div>
  );
});

export default InputArea;
