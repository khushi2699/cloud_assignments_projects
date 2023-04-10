import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout, Button, Space } from 'antd';
import './index.css';
import './index1.css';
import axios from 'axios';

const { Content } = Layout;
const MyPosts = () => {

    const [myPosts, setMyPosts] = useState([]);
    const loadMyEvents = async () => {
        try {
            const token = localStorage.getItem("jwt_token");
            const response = await axios.post(
                "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/myPosts", { token })
            console.log(response)
            if (response.data.statusCode === 400) {
            }
            if (response.data.statusCode === 200) {
                setMyPosts(response.data.items)
            }

        } catch (e) {
            console.log(e)
            console.log(e.response.status)
        }
    };
    const handleDelete = async (postID) => {
        try {
            const response = await axios.post(
                "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/deletePost", { postID })
            console.log(response)
            if (response.data.statusCode === 400) {
            }
            if (response.data.statusCode === 200) {
                loadMyEvents();
            }

        } catch (e) {
            console.log(e)
            console.log(e.response.status)
        }
    };
    const handleSell = async (postID) => {
        try {
            const response = await axios.post(
                "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/sellPost", { postID })
            console.log(response)
            if (response.data.statusCode === 400) {
            }
            if (response.data.statusCode === 200) {
                loadMyEvents();
            }

        } catch (e) {
            console.log(e)
            console.log(e.response.status)
        }
    };
    useEffect(() => {

        loadMyEvents();

    }, [])

    return (
        <Layout>
            <React.Fragment>
                <Content>
                    {console.log(myPosts)}
                    <div className="layout-padding">
                        <h1> Marketplace</h1>
                        <div>
                            <h1>My posts</h1>
                            <div className=" top-boxes full-width horizontal-scroll container">
                                {myPosts.length > 0 ? myPosts
                                    .map((element, index) => (
                                        <div className="full-width single-box">
                                            <div className="full-width" key={element.postID}>
                                                <img className=" center-img" src={element.url} alt="product" />
                                                <div className="earning-text full-width">Product: {element.ProductName}</div>
                                                <div className="earning-text full-width new-line">Category: {element.category}</div>
                                                <div className="earning-text full-width new-line">Price: {element.Price}</div>
                                                <div className="earning-text full-width new-line">Description: {element.Description}</div>
                                                <Space wrap>
                                                    <Button type="primary" onClick={() => handleDelete(element.postID)}>Delete</Button>
                                                </Space>
                                                <Space wrap>
                                                    {element.issold === "true" ? <h3> Sold </h3> : <Button type="primary" onClick={() => handleSell(element.postID)}>Sold</Button> }
                                                </Space>
                                            </div>

                                        </div>
                                    )) : <h2>You have no posts</h2>}

                            </div>

                        </div>

                    </div>
                </Content>
            </React.Fragment>
        </Layout>
    );
};

export default MyPosts;
