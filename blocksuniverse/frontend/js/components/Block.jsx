'use strict';

import React from 'react';
import component from '../util/component.js';
import $ from 'jquery';
import {draggable} from 'jquery-ui'

import InputArea from './InputArea.jsx';

const BlockHelpers = {
  componentDidMount() {
    $(React.findDOMNode(this)).draggable();
  }
}

const Block = component('Block', BlockHelpers, function() {
  return (
    <div className='block-wrapper'>
      <div className='block-stem'>
      </div>
      <InputArea types={['int', 'string', 'bool', 'string', 'int']}/>
    </div>
  );
});

export default Block;
