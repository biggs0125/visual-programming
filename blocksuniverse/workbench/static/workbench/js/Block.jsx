const Block = React.createClass({

  componentDidMount() {
    $(React.findDOMNode(this)).draggable({
      containment: 'parent'
    });
  },
  
  render() {
    return (
      <div className='block'>
        <div className='arrow input-arrow'></div>
        <div className='arrow output-arrow'></div>
      </div>
    );
  }
});
