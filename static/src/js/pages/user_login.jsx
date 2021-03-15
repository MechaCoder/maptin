import React, { Component } from "react";
import ReactDOM from "react-dom";

import {userIdExists, testPassword, validateEmail} from './component/commons.jsx';

export default class Userlogin extends Component {
    constructor() {
        super();
        this.state = {
            'uname': '',
            'pword': '',
            'logged-in': false,
            'hidePassword': true,
        }

        this.testUser = this.testUser.bind(this)
        this.mkUser = this.mkUser.bind(this)
        this.logout = this.logout.bind(this)
        this.showHidePassword = this.showHidePassword.bind(this)
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

        if(this.state.pword.length == 0){
            alert('password is required!')
            return;
        }

        if(testPassword(this.state.pword) == false){
            alert('password needs to contain letters, numbers, and sysbals')
            return;
        }

        if(this.state.uname.length == 0){
            alert('a email is required')
            return;
        }

        if(validateEmail(this.state.uname) == false){
            alert('the email is addr needs to be in valid format.')
            return;
        }


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

    showHidePassword(event){
        this.setState({'hidePassword': !this.state.hidePassword})
    }

    render() {
        var pwHide = 'hide';
        var pwType = 'text'
        if (this.state.hidePassword){
            pwHide = 'show'
            pwType = 'password'
        }



        return (
            <div className="userlogin">
                <div className='inner'>
                    <div className='uname' >
                        <label htmlFor='uname' >username</label>
                        <input name="uname" required={true} type='text' data-error={validateEmail(this.state.uname)} value={this.state.uname} onChange={(event) => {this.setState({'uname': event.target.value})}} />
                    </div>
                    <div className='pword' >
                        <label htmlFor='password' >password</label>
                        <input name="password" required={true} data-error={testPassword(this.state.pword)}  type={pwType} value={this.state.pword} onChange={(event) => {this.setState({'pword': event.target.value})}} />
                        <button onClick={this.showHidePassword}> {pwHide} </button>
                    </div>
                    <div className='btns' >
                        <button onClick={this.testUser} disabled={this.state["logged-in"]} >Sign In</button>
                        <button onClick={this.mkUser} >Sign Up</button>
                    </div>
                </div>
            </div>
        )
    }
}
