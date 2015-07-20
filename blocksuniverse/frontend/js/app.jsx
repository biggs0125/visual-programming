'use strict';

import React from 'react';
import immstruct from 'immstruct';
import Immutable from 'immutable';
import {RouterMixin} from 'react-mini-router';
import component from './util/component.js';

import Workbench from './components/Workbench.jsx';

const State = immstruct('app', {
  blocks: null,
  inputLocations: Immutable.OrderedMap()
});

const AppRoutesMixin = {
  routes: {
    '': 'workbench'
  },
  workbench() {
    return (
      <Workbench inputLocations={State.reference('inputLocations')}/>
    );
  },
  notFound(path) {
    return <div>NOT FOUND: {path}</div>;
  }
};

function renderRoute() {
  return this.renderCurrentRoute();
}

const AppComponent = component('App', [RouterMixin, AppRoutesMixin], renderRoute);

function render() {
  React.render(
    <AppComponent history={true} root=''/>,
    document.getElementById('content')
  );
}

State.on('next-animation-frame', render);
render();
