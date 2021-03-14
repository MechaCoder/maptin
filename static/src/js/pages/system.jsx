import React, { Component } from "react";
import ReactDOM from "react-dom";

export default class System extends Component {
    constructor() {
        super();
        this.state = {
            'users': []
        }
    
    }

    componentDidMount(){

        fetch('/ajax/system/getUsers')
            .then(data=>data.json())
            .then((data)=>{
                console.log(data);
                if(!data.succ){
                    alert(data.err)
                }

                this.setState({
                    'users': data.data.users
                })
            })
        
    }

    resetPassword(event){
        var userid = event.target.getAttribute('data-id');

        if(!confirm('Are you sure you want to reset users password')){
            return;
        }

        // debugger;

        fetch(
            '/ajax/system/updateUserPassword',
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'userId': event.target.getAttribute('data-id')
                }
            }
        )
        .then(data=>data.json())
        .then((json)=>{
            if(!json.succ){
                alert(json.err)
                return;
            }
            alert(json.data.password)
        })

    }


    render() {

        var domEl = []

        for(var i = 0; i <= this.state.users.length; i++){
            var el = this.state.users[i];
            
            if(el == undefined){
                continue;
            }

            domEl.push(
                <tr className='row' data-key={i}>
                    <td>{el.name}</td>
                    <td>{el.email}</td>
                    <td>{el.joined}</td>
                    <td>
                        <button data-id={el.id} onClick={this.resetPassword} >Reset Password</button>
                    </td>
                </tr>
            )
        }

        return (
            <div className="system">
                <div> <h2>System</h2> </div>
                <div className='passwords'>
                    <div>
                        <h2>passwords</h2> 
                        <div>
                            <h3>password reset</h3>
                            <table className='usertable'>
                                <thead className='row header'>
                                    <tr>
                                        <td>Name</td>
                                        <td>email</td>
                                        <td>date joined</td>
                                        <td>actions</td>
                                    </tr>
                                </thead>
                                <thead>
                                    {domEl}
                                </thead>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}