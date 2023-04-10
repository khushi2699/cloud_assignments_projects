import {
    Button,
    Form,
    Input,
} from 'antd';
import AWS from 'aws-sdk';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const { TextArea } = Input;
const formItemLayout = {
    labelCol: {
        xs: {
            span: 24,
        },
        sm: {
            span: 10,
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




let imageUrl = null;

const AddPost = () => {
    const navigate = useNavigate();

    AWS.config.update({
        accessKeyId: 'ASIA5YPJNP3BE3VTRTVH',
        secretAccessKey: 'hc8B4Km6wEygb4EL81pEPff8hPMsg8Sn5vXG0bD1',
        sessionToken: 'FwoGZXIvYXdzEKr//////////wEaDGPtDwjTgbGP/jT+UyLAAQBlnuWetG1bM6CdY9LdeLSvfhWsgGVK/ffnkrqrxdfZX2olHfeBulpxdGu6wotL8/xeJ7WVZuetZ056SG3JhoAHKwGYsoV0bhVcEFjIE/tyzS0jRcDuCqaRk0YYmBGJ30R0ZmIONEjH9FCtm83rRw2d9gZeLl/kqjT0nX9ORaUlh+SkhH+SX/b41Vl7ONxeiDiG/DXMUEy+3EOV8Xij3BssO2NcnvNelOtRyLtuv5+OdR34m7HBU5RLR3H2Uqu34SiBtM2hBjItHFGinoXBO+Q1/An0Tvuv3PIo9kDXo+wvfRfRq353wZMBezS6qBJvZgWE9gbR',
        region: 'us-east-1',
        signatureVersion: 'v4',
    });
    const s3 = new AWS.S3();
    const [imageURL, setImageUrl] = useState(null);
    const [getcategory, setCategory] = useState(null);
    const [file, setFile] = useState(null);
    const [fieldValues, setFieldValues] = useState({
        productName: null,
        price: null,
        description: null,
        category: null
    });

    const handleChange = (e , name) => {
        setFieldValues(prev => ({
        ...prev,
        [name]: e
        }))
      };
    

    useEffect(() => {
    }, [getcategory])

    const handleFileSelect = (e) => {
        setFile(e.target.files[0]);
    }
    const uploadToS3 = async () => {

        console.log(file)
        if (!file) {
            return;
        }
        const params = {
            Bucket: 'cloudproject2023',
            Key: `${Date.now()}.${file.name}`,
            Body: file
        };
        const { Location } = await s3.upload(params).promise();
        setImageUrl(Location);
        imageUrl = Location;
        console.log('uploading to s3', Location);

    }
    const getCategory = async () => {
        try {
            const response = await axios.post(
                "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/getCategory", { imageUrl }
            )
            console.log(response)
            if (response.data.statusCode === 400) {
            }
            if (response.data.statusCode === 200) {
                setCategory(response.data.result)
                handleChange(response.data.result, "category")
            }

        } catch (e) {
            console.log(e)
            console.log(e.response.status)
        }

    }

    const onFinish = (values) => {
        console.log('Received values of form: ', values);
        const savePost = async () => {
            try {
                const token = localStorage.getItem("jwt_token");
                const response = await axios.post(
                    "https://wz6pn6mll3.execute-api.us-east-1.amazonaws.com/Prod/addPost", { fieldValues, imageUrl, token })
                console.log(response)
                if (response.data.statusCode === 400) {
                }
                if (response.data.statusCode === 200) {
                    navigate('/dashboard')
                }

            } catch (e) {
                console.log(e)
                console.log(e.response.status)
            }
        };

        savePost();
    };
    // const [form] = Form.useForm();
    const initialValues = {
        category: getcategory
    };
    return (
        <>
            {console.log(fieldValues)}

            <h2> Add Post</h2>
            <Form
                {...formItemLayout}
                // form={form}
                name="register"
                onFinish={onFinish}
                initialValues={initialValues}
                style={{
                    maxWidth: 600,
                }}
                scrollToFirstError
            >
                <Form.Item
                    name="productName"
                    label="Product Name"
                    rules={[
                        {
                            required: true,
                            message: 'Please input your product name!',
                            whitespace: true,
                        },
                    ]}
                >
                    <Input onChange={(e) => handleChange(e.target.value, "productName")}/>
                </Form.Item>
                <Form.Item
                    name="price"
                    label="Price"
                    rules={[
                        {
                            required: true,
                            message: 'Please input the product price!',
                            whitespace: true,
                        },
                    ]}
                >
                    <Input onChange={(e) => handleChange(e.target.value, "price")}/>
                </Form.Item>
                <Form.Item
                    name="description"
                    label="Description"
                    rules={[
                        {
                            required: true,
                            message: 'Please input the product description!',
                            whitespace: true,
                        },
                    ]}
                >
                    <TextArea rows={4} onChange={(e) => handleChange(e.target.value, "description")}/>
                </Form.Item>
                <Form.Item
                    name="upload"
                    label="Upload"
                    rules={[
                        {
                            required: true,
                            message: 'Please upload a file',
                        },
                    ]}
                >
                    <input type="file" onChange={handleFileSelect} />
                </Form.Item>
                <Form.Item>
                    {file && (
                        <div style={{ marginTop: '10px' }}>
                            <button onClick={uploadToS3}>Upload</button>
                        </div>
                    )}
                </Form.Item>
                <Form.Item>
                    {imageURL && (
                        <div>
                            <button onClick={getCategory}>Get Category</button>
                        </div>
                    )}
                </Form.Item>
                {console.log(getcategory)}
                <Form.Item
                    // name = "getcategory"
                    label="Category"
                    rules={[
                        {
                            required: true,
                            message: 'Please input the category!',
                            whitespace: true,
                        },
                    ]}
                >
                    <Input onChange={(e) => handleChange(e, "category")} value={getcategory} required/>
                </Form.Item>

                <Form.Item {...tailFormItemLayout}>
                    <Button type="primary" htmlType="submit">
                        Register
                    </Button>
                </Form.Item>
            </Form>

        </>
    );
};
export default AddPost;
