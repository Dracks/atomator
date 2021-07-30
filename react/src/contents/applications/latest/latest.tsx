import React from "react"

import { GQLGqlBuild, useGetLatestBuildsQuery } from "../../../utils/graphql/generated"
import GqlHelper from "../../../utils/graphql/helper"
import BuildListWithApp from "./list"

const LatestBuilds: React.FC<{}> = () => {
    const [buildsQuery, reload] = useGetLatestBuildsQuery({
        requestPolicy: "network-only",
    })
    return (
        <GqlHelper query={buildsQuery}>
            {({ data }) => (
                <BuildListWithApp
                    buildsList={data.lastBuilds as GQLGqlBuild[]}
                    reload={reload}
                />
            )}
        </GqlHelper>
    )
}

export default LatestBuilds
