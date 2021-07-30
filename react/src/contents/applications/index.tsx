import { ApmRoute } from "@elastic/apm-rum-react"
import {
    EuiBadge,
    EuiListGroup,
    EuiListGroupItem,
    EuiPageBody,
    EuiPageContent,
    EuiPageContentBody,
    EuiPageSideBar,
} from "@elastic/eui"
import React from "react"
import { Route, Switch, useParams } from "react-router-dom"

import { getRouterLinkProps } from "../../routing"
import { useGetApplicationsQuery } from "../../utils/graphql/generated"
import { LoadingPage } from "../../utils/ui/loading"
import NotFound from "../extra/not-found"
import ApplicationDetails from "./application-details"
import LatestBuilds from "./latest/latest"
import { getVerName } from "./versions/utils"

const SelectAndUser = <T extends { id: number }>(
    name: string,
    data: Array<T>,
    C: React.ElementType,
    other: {} = {},
) => {
    return () => {
        const params = useParams<{ [k: string]: string }>()
        const id = parseInt(params[name], 10)
        console.log(data, id, params)
        const elementList = data.filter(e => e.id === id)
        if (elementList.length > 0) {
            const props = { [name]: elementList[0] }
            return <C {...props} {...other} />
        } else {
            return <NotFound />
        }
    }
}

const ApplicationsIndex: React.FC<{}> = () => {
    const [appsQuery, reload] = useGetApplicationsQuery()
    if (appsQuery.fetching) {
        return <LoadingPage />
    } else {
        const appsList = appsQuery.data.applications!
        return (
            <React.Fragment>
                <EuiPageSideBar>
                    <EuiListGroup flush={false} bordered={true}>
                        <EuiListGroupItem label="List?" />
                        {appsList.map(app => (
                            <EuiListGroupItem
                                key={app.id}
                                label={
                                    <div>
                                        {app.name}
                                        {app.lastRelease && (
                                            <EuiBadge color="primary">
                                                {getVerName(app.lastRelease)}
                                            </EuiBadge>
                                        )}
                                    </div>
                                }
                                {...getRouterLinkProps("/applications/" + app.id)}
                            />
                        ))}
                    </EuiListGroup>
                </EuiPageSideBar>
                <EuiPageBody>
                    <EuiPageContent>
                        <EuiPageContentBody>
                            <Switch>
                                <ApmRoute
                                    path="/applications/"
                                    exact={true}
                                    component={LatestBuilds}
                                />
                                <ApmRoute
                                    path="/applications/:app"
                                    component={SelectAndUser(
                                        "app",
                                        appsList,
                                        ApplicationDetails,
                                        { reload },
                                    )}
                                />
                            </Switch>
                        </EuiPageContentBody>
                    </EuiPageContent>
                </EuiPageBody>
            </React.Fragment>
        )
    }
}

export default ApplicationsIndex
