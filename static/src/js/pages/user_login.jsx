import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class Userlogin extends Component {
    constructor() {
        super();
        this.state = {
            'uname': 'test@anno.com',
            'pword': 'zVuC_evzwa;EF3;h',
            'logged-in': false
            
        }

        this.testUser = this.testUser.bind(this)
        this.mkUser = this.mkUser.bind(this)
        this.logout = this.logout.bind(this)
    }

    componentDidMount(){

        var usr_token = localStorage.getItem('usr_token');
        
        if (usr_token == null ){
            return
        }

        if(usr_token.length != 128){
            return
        }

        fetch('/ajax/user/key', {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'key': usr_token,
            })
        })
        .then(data => data.json())
        .then((json) => {
            console.log(json)
            if(json.succs){
                this.setState({'logged-in': true})
            }
            
        })

    }

    testUser(event){
        
        fetch('/ajax/user', {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'type': 'test',
                'uname': this.state.uname,
                'pword': this.state.pword
            })
        })
        .then(data => data.json())
        .then((json) => {
            if(json.sucss == true){
                localStorage.setItem('usr_token', json.key);
                this.setState({'logged-in': true})
                this.forceUpdate()
            }else{
                alert(json.error)
            }

        })

    }
    mkUser(event){
        
        fetch('/ajax/user', {
            'method': 'POST',
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': JSON.stringify({
                'type': 'create',
                'uname': this.state.uname,
                'pword': this.state.pword
            })
        })
        .then(data => data.json())
        .then((json) => {
            if(json.sucss == true){
                localStorage.setItem('usr_token', json.key);
                this.setState({
                    'logged-in': true,
                })
                this.forceUpdate()
            }else{
                alert(json.error)
            }
            
        })
    }

    logout(){
        localStorage.removeItem('usr_token');
        this.setState({'logged-in': false});
        this.forceUpdate()
    }

    render() {
        if(this.state["logged-in"]){
            return(
                <div className="userlogin" className="loggedin">
                    <button onClick={this.logout}> logout </button>
                </div>
            )
        }

        return (
            <div className="userlogin" className="loggedout" >
                <div>
                    <label htmlFor='uname' >username</label>
                    <input name="uname" type='text' value={this.state.uname} onChange={(event) => {this.setState({'uname': event.target.value})}} />
                </div>
                <div>
                    <label htmlFor='password' >password</label>
                    <input name="password" type='text' value={this.state.pword} onChange={(event) => {this.setState({'pword': event.target.value})}} />   
                </div>
                <div>
                    <button onClick={this.testUser} >Sign In</button>
                    <button onClick={this.mkUser} >Sign Up</button>
                </div>
            </div>
        )
    }
}