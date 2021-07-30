import {
    EuiBadge,
    EuiButton,
    EuiFlexGroup,
    EuiFlexItem,
    EuiPageBody,
    EuiPageContent,
    EuiSelect,
    EuiSteps,
    EuiStepStatus,
    EuiText,
    formatDate,
} from "@elastic/eui"
import { EuiContainedStepProps } from "@elastic/eui/src/components/steps/steps"
import React from "react"
import { useHistory, useParams } from "react-router"

import {
    GQLGqlConfigEnvironment,
    GQLGqlEnvironmentType,
    useGetReleaseConfigsQuery,
    useStartDeployMutation,
} from "../../utils/graphql/generated"
import { getVerName } from "../applications/versions/utils"
import BuildInfo from "../builds/build-info"

const DeployWizard: React.FC<{}> = () => {
    const history = useHistory()
    const { buildId } = useParams()
    const [getConfigsResponse] = useGetReleaseConfigsQuery({
        variables: { buildId: parseInt(buildId, 10) },
    })
    const [_, startDeploy] = useStartDeployMutation()
    const [config, setConfig] = React.useState<number>()
    const [environment, setEnvironment] = React.useState<number>()

    const buildInfo = getConfigsResponse.data?.buildInfo

    const configsList = buildInfo?.application.configurationsSet
    React.useEffect(() => {
        if (configsList && configsList.length === 1) {
            setConfig(configsList[0].id)
        }
    }, [configsList])

    if (!buildInfo) {
        return <div> No Build found </div>
    }

    const environmentsList: Array<Partial<GQLGqlConfigEnvironment>> | undefined =
        configsList &&
        configsList
            .filter(e => e.id === config)
            .reduce(
                (ac, e) =>
                    (ac || e.environments) as Array<Partial<GQLGqlConfigEnvironment>>,
                undefined,
            )
    const environmentStatus: EuiStepStatus = !environment
        ? !config
            ? "disabled"
            : "incomplete"
        : undefined

    const steps: EuiContainedStepProps[] = [
        {
            title: "Config",
            children: (
                <EuiSelect
                    disabled={(configsList && configsList.length === 1) || false}
                    options={
                        (configsList && [
                            { text: "-- select --" },
                            ...configsList.map(e => ({
                                value: e.id,
                                text: e.name,
                            })),
                        ]) ||
                        []
                    }
                    onChange={e => setConfig(parseInt(e.currentTarget.value, 10))}
                    value={config}
                />
            ),
            status: !config ? "incomplete" : undefined,
        },
        {
            title: "Environment",
            children: (
                <EuiSelect
                    options={
                        (environmentsList && [
                            { text: "-- select --" },
                            ...environmentsList.map(e => ({
                                value: e.id,
                                text: e.environment,
                                disabled:
                                    !buildInfo.release &&
                                    e.environment === GQLGqlEnvironmentType.Production,
                            })),
                        ]) ||
                        []
                    }
                    onChange={e => setEnvironment(parseInt(e.currentTarget.value, 10))}
                    value={environment}
                />
            ),
            status: environmentStatus,
        },
        {
            title: "Deploy",
            status: !environment ? "disabled" : "incomplete",
            children: (
                <EuiButton
                    color="danger"
                    disabled={!environment}
                    onClick={() =>
                        startDeploy({
                            buildId,
                            envId: environment,
                        }).then(response => {
                            const resultsId = response.data.startDeploy.resultsId
                            if (resultsId) {
                                history.push("/deploy/" + resultsId)
                            }
                        })
                    }
                >
                    Deploy
                </EuiButton>
            ),
        },
    ]

    return (
        <EuiPageBody>
            <EuiPageContent>
                <EuiFlexGroup wrap>
                    <EuiFlexItem>
                        <EuiSteps steps={steps} />
                    </EuiFlexItem>
                    <EuiFlexItem>
                        <BuildInfo build={buildInfo} />
                    </EuiFlexItem>
                </EuiFlexGroup>
            </EuiPageContent>
        </EuiPageBody>
    )
}

export default DeployWizard
