import {
    Button,
    Form,
    Input,
    Row,
    Col
} from 'antd';
import { useState } from 'react';
import {useNavigate } from 'react-router-dom';
import UserPool from './UserPool';
import { useLocation } from "react-router-dom";
// import { CognitoUserPool, CognitoUserAttribute, CognitoUser } from 'amazon-cognito-identity-js';
// import AmazonCognitoIdentity from 'amazon-cognito-identity-js';


const formItemLayout = {
    labelCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 11,
        },
    },
    wrapperCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 16,
        },
    },
};
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};
const ConfirmUser = () => {
    const emailID = useLocation().state.emailID;
    const navigate = useNavigate();
    const [errors, setErrors] = useState([]);
    const[resendMsg, setResendMsg] = useState([]);
    const [form] = Form.useForm();
    const onFinish = (values) => {
        console.log('Received values of form: ', values);  
        var params = {
            ClientId: '5i536np6ojnnf8pb9mmfj53seu',
            ConfirmationCode: values?.confirmCode,
            Username: values?.email
          };
          const AWS = require('aws-sdk');
          AWS.config.update({region: 'us-east-1'});
          const cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider();
          cognitoIdentityServiceProvider.confirmSignUp(params, function(err, data) {
            if (err) {
                console.log(err, err.stack);
                setErrors(err.message)
            } // an error occurred
            else {
                navigate('/login') 
            }          
          });
    };
    const resendCode = () => {
        var params = {
            ClientId: '5i536np6ojnnf8pb9mmfj53seu',
            Username: emailID
          };
        const AWS = require('aws-sdk');
        AWS.config.update({region: 'us-east-1'});
        const cognitoIdentityServiceProvider = new AWS.CognitoIdentityServiceProvider();
        cognitoIdentityServiceProvider.resendConfirmationCode(params, function(err, data) {
          if (err) {
              console.log(err, err.stack);
              setErrors(err.message)
          } // an error occurred
          else {
            setResendMsg('Successfully resend verfication code! Pls check your email!')
          }          
        }); 
    };

    const initialValues = {
        email: emailID
      };
    return (
        <Row type="flex" justify="center" align="middle" style={{ minHeight: '100vh' }}>
            <Col>
                <div>
                    <h2> Email Verification </h2>
                    {console.log(emailID)}
                    {errors && <h2> {errors}</h2>}
                    {resendMsg && <h2> {resendMsg}</h2>}
                    <Form
                        {...formItemLayout}
                        form={form}
                        name="register"
                        onFinish={onFinish}
                        style={{
                            maxWidth: 600,
                        }}
                        initialValues={initialValues}
                        scrollToFirstError
                    >

                        <Form.Item
                            name="email"
                            label="E-mail"
                            rules={[
                                {
                                    type: 'email',
                                    message: 'The input is not valid E-mail!',
                                },
                                {
                                    required: true,
                                    message: 'Please input your E-mail!',
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>

                        <Form.Item
                            name="confirmCode"
                            label="Confirmation Code"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please input your confirmation code',
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>
                        <h4 role="presentation" onClick={() => resendCode()} className="text-link">Resend Code? </h4>
                        <Form.Item {...tailFormItemLayout}>
                            <Button type="primary" htmlType="submit">
                                Confirm
                            </Button>
                        </Form.Item>
                    </Form>
                </div>
            </Col>
        </Row>
    );
};
export default ConfirmUser;