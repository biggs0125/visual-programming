'use strict';

import React from 'react';
import component from '../util/component.js';
import $ from 'jquery';
import {draggable} from 'jquery-ui'

import InputArea from './InputArea.jsx';
import OutputSlot from './OutputSlot.jsx';

const BlockHelpers = {
    
  updateLocation() {
    const left = React.findDOMNode(this).style.left;
    const top = React.findDOMNode(this).style.top;
    this.props.inputLocations.cursor().update((state) => {
      return state.set(this.slotKey, {top: top, left: left});
    });
  },
  
  componentDidMount() {
    this.slotKey = this.props.inputLocations.cursor().deref().size;
    $(React.findDOMNode(this)).draggable({
      drag: () => {
        this.updateLocation();
      }
    });
    this.updateLocation();
  }
}

const Block = component('Block', BlockHelpers, function({inputTypes, outputType, inputLocations}) {
  return (
    <div className='block-wrapper'>
      <div className='block-body'>
        <div className='block-stem'>
        </div>
        <InputArea types={inputTypes}/>
        <OutputSlot type={outputType}/>
      </div>
    </div>
  );
});

export default Block;
