import {
    EuiAccordion,
    EuiBadge,
    EuiPageBody,
    EuiPageContent,
    EuiText,
} from "@elastic/eui"
import React from "react"
import { useParams } from "react-router"

import {
    GQLGqlExecutionOutput,
    GQLGqlExecutionStatusType,
    GQLGqlTaskStatusType,
    useGetDeployOutputQuery,
} from "../../../utils/graphql/generated"
import GqlHelper from "../../../utils/graphql/helper"
import DeployHead from "./head"

const BadgeStatus: { [key in GQLGqlTaskStatusType]: React.ReactNode } = {
    [GQLGqlTaskStatusType.NothingDone]: <EuiBadge color="hollow">No changes</EuiBadge>,
    [GQLGqlTaskStatusType.Changed]: <EuiBadge color="warning">Changed</EuiBadge>,
    [GQLGqlTaskStatusType.Error]: <EuiBadge color="danger">Error</EuiBadge>,
    [GQLGqlTaskStatusType.Unreachable]: <EuiBadge color="danger">Unreachable</EuiBadge>,
}

const Output: React.FC<{ title: string; message: string }> = ({ title, message }) => (
    <React.Fragment>
        <h4>{title}:</h4>
        <pre>{message}</pre>
    </React.Fragment>
)

const DeployDetails: React.FC<{}> = () => {
    const { deployId } = useParams()
    const requestArgs = { variables: { deployId } }
    const [response, reload] = useGetDeployOutputQuery(requestArgs)

    React.useEffect(() => {
        // console.log(response)
        if (!response.fetching) {
            const deploy = response.data?.deployments[0]
            // console.log(deploy.status)
            if (
                deploy.status === GQLGqlExecutionStatusType.Pending ||
                deploy.status === GQLGqlExecutionStatusType.Working
            ) {
                setTimeout(
                    () => reload({ ...requestArgs, requestPolicy: "network-only" }),
                    5000,
                )
            }
        }
    }, [response])

    return (
        <GqlHelper query={response}>
            {({ data }) => {
                const deploy = data.deployments![0]

                return (
                    <EuiPageContent>
                        <EuiPageBody>
                            <DeployHead deploy={deploy as GQLGqlExecutionOutput} />
                            {deploy.error && (
                                <EuiText>
                                    <Output
                                        title={`Error: ${deploy.error.message}`}
                                        message={deploy.error.stacktrace}
                                    />
                                </EuiText>
                            )}
                            {deploy.taskoutputSet.map(
                                ({
                                    name,
                                    message,
                                    stdout,
                                    stderr,
                                    status,
                                    id,
                                    machine,
                                }) => (
                                    <EuiAccordion
                                        key={id}
                                        id={`accordionForm${id}`}
                                        className="euiAccordionForm"
                                        buttonClassName="euiAccordionForm__button"
                                        buttonContent={`[${machine.name}] ${name}`}
                                        extraAction={BadgeStatus[status]}
                                        paddingSize="l"
                                    >
                                        <EuiText>
                                            {message && (
                                                <Output
                                                    title="Message"
                                                    message={message}
                                                />
                                            )}
                                            {stdout && (
                                                <Output
                                                    title="Standard output"
                                                    message={stdout}
                                                />
                                            )}
                                            {stderr && (
                                                <Output
                                                    title="Standard error"
                                                    message={stderr}
                                                />
                                            )}
                                            {!message && !stderr && !stdout && (
                                                <h3>No output for this task</h3>
                                            )}
                                        </EuiText>
                                    </EuiAccordion>
                                ),
                            )}
                        </EuiPageBody>
                    </EuiPageContent>
                )
            }}
        </GqlHelper>
    )
}
export default DeployDetails
