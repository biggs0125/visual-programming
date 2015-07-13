const Block = React.createClass({
  render() {
    return (
      <div>This is a block!</div>
    );
  }
});

const Workbench = React.createClass({
  render() {
    return (
      <Block/>
    );
  }
});

React.render(
  <Workbench/>,
  document.getElementById('content')
);
