'use strict';

import React from 'react';
import component from '../util/component.js';
import $ from 'jquery';
import {draggable} from 'jquery-ui'

import InputArea from './InputArea.jsx';
import OutputSlot from './OutputSlot.jsx';

const BlockHelpers = {
  componentDidMount() {
    $(React.findDOMNode(this)).draggable();
  }
}

const Block = component('Block', BlockHelpers, function() {
  return (
    <div className='block-wrapper'>
      <div className='block-body'>
        <div className='block-stem'>
        </div>
        <InputArea types={['INT', 'STRING', 'BOOL', 'STRING', 'INT']}/>
        <OutputSlot type={'STRING'}/>
      </div>
    </div>
  );
});

export default Block;
