import {Input, Skeleton} from 'antd';
import React from "react";
import ImmersiveReader from "./ImmersiveReader";

const {Search} = Input;

class Analyser extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            loadingState: false,
            value: '',
            disabledState: true
        };

        this.onPressEnter = this.onPressEnter.bind(this);
        this.onSearch = this.onSearch.bind(this);
        this.onChange = this.onChange.bind(this);
    }

    onSearch = (value, e) => {
        this.setState({loadingState: true});
        this.submitRequest();
    }

    submitRequest() {
        fetch("http://127.0.0.1:5000/analysis?url=" + this.state.value)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        loadingState: false,
                        text: result.string,
                        title: result.title,
                        disabledState: false
                    });
                },
                (error) => {
                    this.setState({
                        loadingState: false
                    });
                    console.log(error);
                }
            )
    }

    onPressEnter() {
        this.setState({loadingState: true});
        this.onSearch();
    }

    onChange = e => {
        this.setState({value: e.target.value});
    }

    render() {
        return (<div>
                <Search placeholder="input url" enterButton="Analyse"
                        onPressEnter={this.onPressEnter} size="large"
                        style={{width: "75%"}}
                        onSearch={this.onSearch}
                        onChange={this.onChange}
                        loading={this.state.loadingState}/>
                <ImmersiveReader
                    style={{height: '40px'}}
                    title={this.state.title}
                    text={this.state.text}
                    locale={"en"}
                    tokenURL="http://127.0.0.1:5000/GetTokenAndSubdomain"
                    disabled={this.state.disabledState}
                />
                <div className="article">
                    <Skeleton active loading={this.state.loadingState}>
                        <p style={{whiteSpace: "pre-wrap", fontSize: 'medium'}}>{this.state.text}</p>
                    </Skeleton>
                </div>
            </div>
        )
            ;
    }
}

export default Analyser;
