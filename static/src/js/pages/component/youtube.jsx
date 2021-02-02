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
            <iframe width="250" height="250" src={ytv} frameBorder="0"></iframe>
        )
    }
}