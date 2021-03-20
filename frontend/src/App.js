import './App.css';
import {Layout, Menu, Breadcrumb} from "antd";

import 'antd/dist/antd.css';
import Home from "./Home.js";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from 'react-router-dom';
import Bot from "./Bot";

const {Header, Footer, Content} = Layout;

function App() {
    return (
        <Router>
            <Layout className="layout">
                <Header>
                    <div className="logo"/>
                    <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
                        <Menu.Item key="1"><Link to="/">Home</Link></Menu.Item>
                        <Menu.Item key="2"><Link to="/chatbot">Chatbot</Link></Menu.Item>
                        <Menu.Item key="3"><Link to="/webanalyser">Extract info</Link></Menu.Item>
                    </Menu>
                </Header>
                <Content style={{padding: '0 50px'}}>
                    <Breadcrumb style={{margin: '16px 0'}}>
                        <Breadcrumb.Item>Home</Breadcrumb.Item>
                        <Breadcrumb.Item>List</Breadcrumb.Item>
                        <Breadcrumb.Item>App</Breadcrumb.Item>
                    </Breadcrumb>
                    <div className="site-layout-content">
                        <Switch>
                            <Route path="/webanalyser">
                                Dan
                            </Route>
                            <Route path="/chatbot">
                                <Bot/>
                            </Route>
                            <Route path="/">
                                <Home/>
                            </Route>
                        </Switch>
                    </div>
                    <Footer style={{textAlign: 'center'}}>fooBar (C) 2021</Footer>
                </Content>
            </Layout>
        </Router>);
}


export default App;
