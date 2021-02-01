import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class MapListItem extends Component {
    constructor() {
        super();
    }

    render() {
        return (
            <div className="MapListItem" data-hex={this.props.hex}>
                <a href="/">
                    <div> <img src={this.props.map} width='200px' /></div>
                    <div>{this.props.title}</div>

                </a>
            </div>
        )
    }
}