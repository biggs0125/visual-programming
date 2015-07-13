const Block = React.createClass({displayName: 'Block',
  render() {
    return (
      React.createElement("div", null, "This is a block!")
    );
  }
});

const Workbench = React.createClass({displayName: 'Workbench',
  render() {
    return (
      React.createElement(Block, null)
    );
  }
});

React.render(
  React.createElement(Workbench, null),
  document.getElementById('content')
);
