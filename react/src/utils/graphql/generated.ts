import gql from "graphql-tag"
import * as Urql from "urql"
export type Maybe<T> = T | null
export type Omit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
    ID: string
    String: string
    Boolean: boolean
    Int: number
    Float: number
    DateTime: any
}

export enum GQLBuildChange {
    A_0 = "A_0",
    A_1 = "A_1",
    A_2 = "A_2",
}

export type GQLGqlAppConfig = {
    __typename?: "GQLAppConfig"
    id: Scalars["Int"]
    application: GQLGqlApplication
    name: Scalars["String"]
    tagsList: Array<GQLGqlConfigTag>
    environments: Array<GQLGqlConfigEnvironment>
}

export type GQLGqlApplication = {
    __typename?: "GQLApplication"
    id: Scalars["Int"]
    name: Scalars["String"]
    releaseBranch: Scalars["String"]
    tokenSet: Array<GQLGqlToken>
    repositorySet: Array<GQLGqlRepository>
    buildSet: Array<GQLGqlBuild>
    configurationsSet: Array<GQLGqlAppConfig>
    lastRelease?: Maybe<GQLGqlBuild>
    lastBuild?: Maybe<GQLGqlBuild>
}

export type GQLGqlBuild = {
    __typename?: "GQLBuild"
    id: Scalars["Int"]
    application: GQLGqlApplication
    date: Scalars["DateTime"]
    major: Scalars["Int"]
    minor: Scalars["Int"]
    patch: Scalars["Int"]
    commit: Scalars["String"]
    branch: Scalars["String"]
    release: Scalars["Boolean"]
    change: GQLBuildChange
    file?: Maybe<GQLGqlFileInfo>
    changesList: Array<GQLGqlChange>
    machineSet: Array<GQLGqlMachine>
    isReleasable: Scalars["Boolean"]
}

export type GQLGqlChange = {
    __typename?: "GQLChange"
    id: Scalars["ID"]
    type?: Maybe<GQLGqlChangeType>
    description: Scalars["String"]
}

export enum GQLGqlChangeType {
    Fix = "fix",
    Improvement = "improvement",
    NewFeature = "new_feature",
    Unknown = "unknown",
}

export type GQLGqlConfigEnvironment = {
    __typename?: "GQLConfigEnvironment"
    id: Scalars["ID"]
    environment?: Maybe<GQLGqlEnvironmentType>
    configuration: GQLGqlAppConfig
    executionoutputSet: Array<GQLGqlExecutionOutput>
}

export type GQLGqlConfigTag = {
    __typename?: "GQLConfigTag"
    id: Scalars["ID"]
    name: Scalars["String"]
}

export enum GQLGqlEnvironmentType {
    Devel = "devel",
    Staging = "staging",
    Production = "production",
}

export type GQLGqlExecutionError = {
    __typename?: "GQLExecutionError"
    id: Scalars["Int"]
    message: Scalars["String"]
    stacktrace: Scalars["String"]
}

export type GQLGqlExecutionOutput = {
    __typename?: "GQLExecutionOutput"
    id: Scalars["Int"]
    status: GQLGqlExecutionStatusType
    environment: GQLGqlConfigEnvironment
    date: Scalars["DateTime"]
    build?: Maybe<GQLGqlBuild>
    application?: Maybe<GQLGqlApplication>
    error?: Maybe<GQLGqlExecutionError>
    taskoutputSet: Array<GQLGqlTaskOutput>
}

export enum GQLGqlExecutionStatusType {
    Pending = "pending",
    Working = "working",
    Ok = "ok",
    Error = "error",
}

export type GQLGqlFileInfo = {
    __typename?: "GQLFileInfo"
    id: Scalars["ID"]
    name: Scalars["String"]
    size: Scalars["Int"]
    contentType: Scalars["String"]
    url: Scalars["String"]
}

export type GQLGqlMachine = {
    __typename?: "GQLMachine"
    id: Scalars["ID"]
    name: Scalars["String"]
}

export type GQLGqlRepository = {
    __typename?: "GQLRepository"
    id: Scalars["ID"]
    applications: Array<GQLGqlApplication>
    provider: GQLRepositoryProvider
    name: Scalars["String"]
    url: Scalars["String"]
}

export type GQLGqlTaskOutput = {
    __typename?: "GQLTaskOutput"
    id: Scalars["Int"]
    machine: GQLGqlMachine
    name: Scalars["String"]
    status: GQLGqlTaskStatusType
    stdout?: Maybe<Scalars["String"]>
    stderr?: Maybe<Scalars["String"]>
    message?: Maybe<Scalars["String"]>
    appName: Scalars["String"]
}

export enum GQLGqlTaskStatusType {
    NothingDone = "nothing_done",
    Changed = "changed",
    Error = "error",
    Unreachable = "unreachable",
}

export type GQLGqlToken = {
    __typename?: "GQLToken"
    id: Scalars["ID"]
    name?: Maybe<Scalars["String"]>
    token: Scalars["String"]
}

export type GQLLogin = {
    __typename?: "Login"
    profile?: Maybe<GQLMyProfileType>
    error?: Maybe<GQLLoginErrorType>
}

export type GQLLoginErrorType = {
    __typename?: "LoginErrorType"
    code: Scalars["Int"]
    message: Scalars["String"]
}

export type GQLLogout = {
    __typename?: "Logout"
    status?: Maybe<Scalars["String"]>
}

export type GQLMutation = {
    __typename?: "Mutation"
    session?: Maybe<GQLSession>
    startDeploy?: Maybe<GQLStartDeploy>
    releaseBuild?: Maybe<GQLReleaseBuild>
}

export type GQLMutationStartDeployArgs = {
    buildId: Scalars["Int"]
    environmentId: Scalars["Int"]
}

export type GQLMutationReleaseBuildArgs = {
    buildId: Scalars["Int"]
}

export type GQLMyProfileType = {
    __typename?: "MyProfileType"
    id: Scalars["ID"]
    lastLogin?: Maybe<Scalars["DateTime"]>
    isSuperuser: Scalars["Boolean"]
    username: Scalars["String"]
    firstName: Scalars["String"]
    lastName: Scalars["String"]
    email: Scalars["String"]
    isStaff: Scalars["Boolean"]
    dateJoined: Scalars["DateTime"]
}

export type GQLQuery = {
    __typename?: "Query"
    applications: Array<GQLGqlApplication>
    buildInfo?: Maybe<GQLGqlBuild>
    lastBuilds?: Maybe<Array<GQLGqlBuild>>
    deployments?: Maybe<Array<GQLGqlExecutionOutput>>
    myProfile?: Maybe<GQLMyProfileType>
}

export type GQLQueryBuildInfoArgs = {
    buildId: Scalars["Int"]
}

export type GQLQueryDeploymentsArgs = {
    deployId?: Maybe<Scalars["Int"]>
    fromDt?: Maybe<Scalars["DateTime"]>
}

export type GQLReleaseBuild = {
    __typename?: "ReleaseBuild"
    build?: Maybe<GQLGqlBuild>
    error?: Maybe<Scalars["String"]>
}

export enum GQLRepositoryProvider {
    A_0 = "A_0",
}

export type GQLSession = {
    __typename?: "Session"
    login?: Maybe<GQLLogin>
    logout?: Maybe<GQLLogout>
}

export type GQLSessionLoginArgs = {
    password: Scalars["String"]
    username: Scalars["String"]
}

export type GQLStartDeploy = {
    __typename?: "StartDeploy"
    resultsId?: Maybe<Scalars["Int"]>
}

export const GetApplicationsDocument = gql`
    query GetApplications {
        applications {
            id
            name
            releaseBranch
            tokenSet {
                id
                name
                token
            }
            repositorySet {
                id
                name
                provider
                url
            }
            lastBuild {
                id
                major
                minor
                patch
            }
            lastRelease {
                id
                major
                minor
                patch
            }
            buildSet {
                id
                date
                major
                minor
                patch
                branch
                release
                changesList {
                    type
                    description
                }
                file {
                    size
                    name
                    url
                }
            }
        }
    }
`

export function useGetApplicationsQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetApplicationsQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetApplicationsQuery>({
        query: GetApplicationsDocument,
        ...options,
    })
}
export const ReleaseBuildDocument = gql`
    mutation ReleaseBuild($buildId: Int!) {
        releaseBuild(buildId: $buildId) {
            build {
                release
            }
        }
    }
`

export function useReleaseBuildMutation() {
    return Urql.useMutation<GQLReleaseBuildMutation, GQLReleaseBuildMutationVariables>(
        ReleaseBuildDocument,
    )
}
export const GetLatestBuildsDocument = gql`
    query GetLatestBuilds {
        lastBuilds {
            id
            application {
                id
                name
            }
            major
            minor
            patch
            release
            isReleasable
            branch
            date
            file {
                size
                name
                url
            }
        }
    }
`

export function useGetLatestBuildsQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetLatestBuildsQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetLatestBuildsQuery>({
        query: GetLatestBuildsDocument,
        ...options,
    })
}
export const GetReleaseConfigsDocument = gql`
    query getReleaseConfigs($buildId: Int!) {
        buildInfo(buildId: $buildId) {
            major
            minor
            patch
            date
            release
            application {
                name
                configurationsSet {
                    id
                    name
                    environments {
                        id
                        environment
                    }
                }
            }
            changes: changesList {
                type
                description
            }
        }
    }
`

export function useGetReleaseConfigsQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetReleaseConfigsQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetReleaseConfigsQuery>({
        query: GetReleaseConfigsDocument,
        ...options,
    })
}
export const StartDeployDocument = gql`
    mutation startDeploy($buildId: Int!, $envId: Int!) {
        startDeploy(buildId: $buildId, environmentId: $envId) {
            resultsId
        }
    }
`

export function useStartDeployMutation() {
    return Urql.useMutation<GQLStartDeployMutation, GQLStartDeployMutationVariables>(
        StartDeployDocument,
    )
}
export const GetListDeploysDocument = gql`
    query getListDeploys($fromDate: DateTime) {
        deployments(fromDt: $fromDate) {
            id
            status
            application {
                name
            }
            environment {
                environment
            }
            date
        }
    }
`

export function useGetListDeploysQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetListDeploysQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetListDeploysQuery>({
        query: GetListDeploysDocument,
        ...options,
    })
}
export const GetDeployOutputDocument = gql`
    query getDeployOutput($deployId: Int!) {
        deployments(deployId: $deployId) {
            id
            status
            environment {
                environment
            }
            date
            error {
                message
                stacktrace
            }
            application {
                name
            }
            build {
                major
                minor
                patch
            }
            taskoutputSet {
                id
                name
                status
                stdout
                stderr
                message
                machine {
                    name
                }
            }
        }
    }
`

export function useGetDeployOutputQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetDeployOutputQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetDeployOutputQuery>({
        query: GetDeployOutputDocument,
        ...options,
    })
}
export const GetUserInfoDocument = gql`
    query getUserInfo {
        myProfile {
            username
        }
    }
`

export function useGetUserInfoQuery(
    options: Omit<Urql.UseQueryArgs<GQLGetUserInfoQueryVariables>, "query"> = {},
) {
    return Urql.useQuery<GQLGetUserInfoQuery>({
        query: GetUserInfoDocument,
        ...options,
    })
}
export const LogInDocument = gql`
    mutation logIn($username: String!, $password: String!) {
        session {
            login(username: $username, password: $password) {
                profile {
                    username
                }
                error {
                    code
                }
            }
        }
    }
`

export function useLogInMutation() {
    return Urql.useMutation<GQLLogInMutation, GQLLogInMutationVariables>(LogInDocument)
}
export const LogOutDocument = gql`
    mutation logOut {
        session {
            logout {
                status
            }
        }
    }
`

export function useLogOutMutation() {
    return Urql.useMutation<GQLLogOutMutation, GQLLogOutMutationVariables>(
        LogOutDocument,
    )
}
export type GQLGetApplicationsQueryVariables = {}

export type GQLGetApplicationsQuery = { __typename?: "Query" } & {
    applications: Array<
        { __typename?: "GQLApplication" } & Pick<
            GQLGqlApplication,
            "id" | "name" | "releaseBranch"
        > & {
                tokenSet: Array<
                    { __typename?: "GQLToken" } & Pick<
                        GQLGqlToken,
                        "id" | "name" | "token"
                    >
                >
                repositorySet: Array<
                    { __typename?: "GQLRepository" } & Pick<
                        GQLGqlRepository,
                        "id" | "name" | "provider" | "url"
                    >
                >
                lastBuild?: Maybe<
                    { __typename?: "GQLBuild" } & Pick<
                        GQLGqlBuild,
                        "id" | "major" | "minor" | "patch"
                    >
                >
                lastRelease?: Maybe<
                    { __typename?: "GQLBuild" } & Pick<
                        GQLGqlBuild,
                        "id" | "major" | "minor" | "patch"
                    >
                >
                buildSet: Array<
                    { __typename?: "GQLBuild" } & Pick<
                        GQLGqlBuild,
                        | "id"
                        | "date"
                        | "major"
                        | "minor"
                        | "patch"
                        | "branch"
                        | "release"
                    > & {
                            changesList: Array<
                                { __typename?: "GQLChange" } & Pick<
                                    GQLGqlChange,
                                    "type" | "description"
                                >
                            >
                            file?: Maybe<
                                { __typename?: "GQLFileInfo" } & Pick<
                                    GQLGqlFileInfo,
                                    "size" | "name" | "url"
                                >
                            >
                        }
                >
            }
    >
}

export type GQLReleaseBuildMutationVariables = {
    buildId: Scalars["Int"]
}

export type GQLReleaseBuildMutation = { __typename?: "Mutation" } & {
    releaseBuild?: Maybe<
        { __typename?: "ReleaseBuild" } & {
            build?: Maybe<{ __typename?: "GQLBuild" } & Pick<GQLGqlBuild, "release">>
        }
    >
}

export type GQLGetLatestBuildsQueryVariables = {}

export type GQLGetLatestBuildsQuery = { __typename?: "Query" } & {
    lastBuilds?: Maybe<
        Array<
            { __typename?: "GQLBuild" } & Pick<
                GQLGqlBuild,
                | "id"
                | "major"
                | "minor"
                | "patch"
                | "release"
                | "isReleasable"
                | "branch"
                | "date"
            > & {
                    application: { __typename?: "GQLApplication" } & Pick<
                        GQLGqlApplication,
                        "id" | "name"
                    >
                    file?: Maybe<
                        { __typename?: "GQLFileInfo" } & Pick<
                            GQLGqlFileInfo,
                            "size" | "name" | "url"
                        >
                    >
                }
        >
    >
}

export type GQLGetReleaseConfigsQueryVariables = {
    buildId: Scalars["Int"]
}

export type GQLGetReleaseConfigsQuery = { __typename?: "Query" } & {
    buildInfo?: Maybe<
        { __typename?: "GQLBuild" } & Pick<
            GQLGqlBuild,
            "major" | "minor" | "patch" | "date" | "release"
        > & {
                application: { __typename?: "GQLApplication" } & Pick<
                    GQLGqlApplication,
                    "name"
                > & {
                        configurationsSet: Array<
                            { __typename?: "GQLAppConfig" } & Pick<
                                GQLGqlAppConfig,
                                "id" | "name"
                            > & {
                                    environments: Array<
                                        { __typename?: "GQLConfigEnvironment" } & Pick<
                                            GQLGqlConfigEnvironment,
                                            "id" | "environment"
                                        >
                                    >
                                }
                        >
                    }
                changes: Array<
                    { __typename?: "GQLChange" } & Pick<
                        GQLGqlChange,
                        "type" | "description"
                    >
                >
            }
    >
}

export type GQLStartDeployMutationVariables = {
    buildId: Scalars["Int"]
    envId: Scalars["Int"]
}

export type GQLStartDeployMutation = { __typename?: "Mutation" } & {
    startDeploy?: Maybe<
        { __typename?: "StartDeploy" } & Pick<GQLStartDeploy, "resultsId">
    >
}

export type GQLGetListDeploysQueryVariables = {
    fromDate?: Maybe<Scalars["DateTime"]>
}

export type GQLGetListDeploysQuery = { __typename?: "Query" } & {
    deployments?: Maybe<
        Array<
            { __typename?: "GQLExecutionOutput" } & Pick<
                GQLGqlExecutionOutput,
                "id" | "status" | "date"
            > & {
                    application?: Maybe<
                        { __typename?: "GQLApplication" } & Pick<
                            GQLGqlApplication,
                            "name"
                        >
                    >
                    environment: { __typename?: "GQLConfigEnvironment" } & Pick<
                        GQLGqlConfigEnvironment,
                        "environment"
                    >
                }
        >
    >
}

export type GQLGetDeployOutputQueryVariables = {
    deployId: Scalars["Int"]
}

export type GQLGetDeployOutputQuery = { __typename?: "Query" } & {
    deployments?: Maybe<
        Array<
            { __typename?: "GQLExecutionOutput" } & Pick<
                GQLGqlExecutionOutput,
                "id" | "status" | "date"
            > & {
                    environment: { __typename?: "GQLConfigEnvironment" } & Pick<
                        GQLGqlConfigEnvironment,
                        "environment"
                    >
                    error?: Maybe<
                        { __typename?: "GQLExecutionError" } & Pick<
                            GQLGqlExecutionError,
                            "message" | "stacktrace"
                        >
                    >
                    application?: Maybe<
                        { __typename?: "GQLApplication" } & Pick<
                            GQLGqlApplication,
                            "name"
                        >
                    >
                    build?: Maybe<
                        { __typename?: "GQLBuild" } & Pick<
                            GQLGqlBuild,
                            "major" | "minor" | "patch"
                        >
                    >
                    taskoutputSet: Array<
                        { __typename?: "GQLTaskOutput" } & Pick<
                            GQLGqlTaskOutput,
                            "id" | "name" | "status" | "stdout" | "stderr" | "message"
                        > & {
                                machine: { __typename?: "GQLMachine" } & Pick<
                                    GQLGqlMachine,
                                    "name"
                                >
                            }
                    >
                }
        >
    >
}

export type GQLGetUserInfoQueryVariables = {}

export type GQLGetUserInfoQuery = { __typename?: "Query" } & {
    myProfile?: Maybe<
        { __typename?: "MyProfileType" } & Pick<GQLMyProfileType, "username">
    >
}

export type GQLLogInMutationVariables = {
    username: Scalars["String"]
    password: Scalars["String"]
}

export type GQLLogInMutation = { __typename?: "Mutation" } & {
    session?: Maybe<
        { __typename?: "Session" } & {
            login?: Maybe<
                { __typename?: "Login" } & {
                    profile?: Maybe<
                        { __typename?: "MyProfileType" } & Pick<
                            GQLMyProfileType,
                            "username"
                        >
                    >
                    error?: Maybe<
                        { __typename?: "LoginErrorType" } & Pick<
                            GQLLoginErrorType,
                            "code"
                        >
                    >
                }
            >
        }
    >
}

export type GQLLogOutMutationVariables = {}

export type GQLLogOutMutation = { __typename?: "Mutation" } & {
    session?: Maybe<
        { __typename?: "Session" } & {
            logout?: Maybe<{ __typename?: "Logout" } & Pick<GQLLogout, "status">>
        }
    >
}
