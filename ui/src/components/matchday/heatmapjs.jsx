import ReactDOM, { render } from 'react-dom';
import React, {useState, useEffect} from 'react';
import { isEmpty } from '../sharedfunctions.js';
// import React, {Component, PropTypes} from 'react';
import h337 from 'heatmap.js'

/* export class HeatmapJs extends Component {

  constructor(props, context) {
    super(props, context);
    this.state = { cfg: null };
  }

  componentDidMount(){
    const { style, data, config } = this.props;
    let c = config || {};
    let _container = ReactDOM.findDOMNode(this);
    console.log(_container)
    let defaultCfg = {
      // width: style.width.replace('px','') || _container.offsetWidth,
      // height: style.height.replace('px','') || _container.offsetHeight,
    };
    // let _cfg = _.merge( defaultCfg, c );
    let _cfg = {}
    _cfg.container = document.querySelector('.jsheatmap');
    console.log(_cfg)
    this.heatmapInstance = h337.create(_cfg);
    this.setState({ cfg: _cfg });
    this.heatmapInstance.setData( data );
  }

  componentWillReceiveProps(nextProps){
    return nextProps != this.props;
  }

  shouldComponentUpdate(nextProps){
    return nextProps != this.props;
  }

  render(){

    return (
      <div className="jsheatmap"></div>
    );

  }

} */

export const HeatmapJs = ({ style, data, config }) => {

  let _cfg = {gradient: { 0.55: "rgb(77,123,187)", 0.7: "rgb(239,218,226)", 0.8: "rgb(224,184,200)", 0.9: "rgb(210,148,172)", 0.95: "rgb(194,112,145)", 1.0: "rgb(180,77,117)"}}

  useEffect(() => {
    console.log('useeffect - initial')
    // _cfg.container = document.querySelector('.jsheatmap');

  }, [])

  useEffect(() => {
    console.log('useeffect - data')
    _cfg.container = document.querySelector('.jsheatmap');
    var heatmapInstance = h337.create(_cfg)
    // heatmapInstance = null
    // var heatmapInstance = h337.create(_cfg)
    heatmapInstance.setData( data );

  }, [data])


  return (<div className="w3-margin jsheatmap"></div>)
}
