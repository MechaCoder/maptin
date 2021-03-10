import React, { Component } from "react";
import ReactDOM from "react-dom";
import MapListItem from "./component/map_list_item.jsx";
import {getUserId} from './component/commons.jsx'

export default class MapsList extends Component {
    constructor() {
        super();
        this.state = {
            'hide': false,
            'maps': []
        }
        this.createMap = this.createMap.bind(this)
        this.getMaps = this.getMaps.bind(this)
    }

    componentDidMount(){
        this.getMaps();
    }

    getMaps(){
        var usr_token = getUserId();
        
        fetch('/ajax/maps', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            }
        })
        .then(data => data.json())
        .then((json) => {
            this.setState({
                'maps': json
            })

        })
    }

    createMap(event){

        var usr_token = getUserId();
        
        fetch('/ajax/maps', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'userKey': usr_token
            }
        })
        .then(data => data.json())
        .then((json) => {
            alert('new map has been created')
            // TODO: script out reading maps
            this.getMaps()
        })

    }

    render() {

        if(this.state.hide){
            return(<div>maps</div>)
        }
        
        var items = []
        for(var i = 0; i < this.state.maps.length; i++){
            var el = this.state.maps[i];
            items.push(<MapListItem 
                key={i} 
                hex={el.hex} 
                title={el.title} 
                map={el.map_source} 
                soundtrack={el.map_soundtrack} 
            />)

        }

        return (    
            <div className="maps_diolog">
                <div className='maps_row'>
                    <div id='newMap' onClick={this.createMap}>Create Map</div>
                    {items}
                </div>
            </div>
        )
    }
}