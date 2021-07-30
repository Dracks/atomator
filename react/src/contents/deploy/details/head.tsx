import {
    EuiFlexGroup,
    EuiFlexItem,
    EuiIcon,
    EuiText,
    EuiToolTip,
    formatDate,
} from "@elastic/eui"
import React from "react"

import {
    GQLGqlExecutionOutput,
    GQLGqlExecutionStatusType,
} from "../../../utils/graphql/generated"
import { getVerName } from "../../applications/versions/utils"

interface DeployHeadProps {
    deploy: GQLGqlExecutionOutput
}
const DeployHead: React.FC<DeployHeadProps> = ({ deploy }) => (
    <EuiFlexGroup>
        <EuiFlexItem>
            <EuiText>
                <h2>{deploy.application && deploy.application.name} </h2>
                Environment: {deploy.environment.environment}
                <br />
                Status: {deploy.status}
                <EuiToolTip
                    position="bottom"
                    content={Object.keys(GQLGqlExecutionStatusType).reduce(
                        (ac, e) => ac + "/" + e,
                    )}
                >
                    <EuiIcon tabIndex={0} type="questionInCircle" />
                </EuiToolTip>
                <br />
            </EuiText>
        </EuiFlexItem>
        <EuiFlexItem>
            <EuiText>
                <h3>{deploy.build && getVerName(deploy.build)}</h3>
                {formatDate(deploy.date, "dateTime")}
            </EuiText>
        </EuiFlexItem>
    </EuiFlexGroup>
)

export default DeployHead
