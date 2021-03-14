import React, { Component } from "react";
import ReactDOM from "react-dom";

import {userIdExists} from './component/commons.jsx';

export default class Userlogin extends Component {
    constructor() {
        super();
        this.state = {
            'uname': 'test@testserver.com',
            'pword': 'password1234',
            'logged-in': false
        }

        this.testUser = this.testUser.bind(this)
        this.mkUser = this.mkUser.bind(this)
        this.logout = this.logout.bind(this)
    }

    componentDidUpdate(){
        if(this.state['logged-in']){
            window.location.href = '/dashboard/'
        }
    }

    componentDidMount(){

        if(userIdExists()){
            // if the user key already set on the client then use it
            window.location.href = '/dashboard/' 
        }

        var usr_token = localStorage.getItem('usr_token');

        if (usr_token == null ){
            return
        }

        if(usr_token.length != 128){
            return
        }

        fetch('/ajax/user/key', { // tests key
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
            if(json.succs){
                this.setState({'logged-in': true})
                return;
            }else{
                alert(json.err)
                this.setState({'logged-in': false})
                return;
            }
        })

    }

    testUser(event){
        console.log('testUser');

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
            if(json.succ == true){
                localStorage.setItem('usr_token', json.data.key);
                this.setState({'logged-in': true})
                this.forceUpdate()
            }else{
                alert(json.err)
            }

        })

    } // testUser
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
            if(json.succ == true){

                localStorage.setItem('usr_token', json.data.key);
                this.setState({
                    'logged-in': true,
                })
                this.forceUpdate()
            }else{
                alert(json.err)
            }

        })
    } // mkUser

    logout(){
        localStorage.removeItem('usr_token');
        this.setState({'logged-in': false});
        this.forceUpdate()
    }

    render() {

        return (
            <div className="userlogin">
                <div className='uname' >
                    <label htmlFor='uname' >username</label>
                    <input name="uname" type='text' value={this.state.uname} onChange={(event) => {this.setState({'uname': event.target.value})}} />
                </div>
                <div className='pword' >
                    <label htmlFor='password' >password</label>
                    <input name="password" type='text' value={this.state.pword} onChange={(event) => {this.setState({'pword': event.target.value})}} />
                </div>
                <div className='btns' >
                    <button onClick={this.testUser} disabled={this.state["logged-in"]} >Sign In</button>
                    <button onClick={this.mkUser} >Sign Up</button>
                </div>
            </div>
        )
    }
}
