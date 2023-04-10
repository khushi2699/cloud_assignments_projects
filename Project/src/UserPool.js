import { CognitoUserPool } from "amazon-cognito-identity-js";

const poolData = {
    UserPoolId: "us-east-1_WaRPrCUfk",
    ClientId: "5i536np6ojnnf8pb9mmfj53seu"
}

export default new CognitoUserPool(poolData);