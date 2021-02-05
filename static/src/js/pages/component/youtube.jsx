import React, { Component } from "react";
import ReactDOM from "react-dom";

const youtubeEmbed = require('youtube-embed')

export default class Youtube extends Component {
    constructor() {
        super();
    }

    render() {
        var ytv = youtubeEmbed(this.props.url);
        return (
            <iframe 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                width="125" 
                height="125"
                src={ytv} 
                frameBorder="0"
            ></iframe>
        )
    }
}