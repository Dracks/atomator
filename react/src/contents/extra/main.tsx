import {
    EuiPageContent,
    EuiPageContentBody,
    EuiPageContentHeader,
    EuiPageContentHeaderSection,
    EuiTitle,
} from "@elastic/eui"
import React from "react"

const MainPage: React.FC<{}> = () => (
    <EuiPageContent>
        <EuiPageContentHeader>
            <EuiPageContentHeaderSection>
                <EuiTitle>
                    <h2>Content title</h2>
                </EuiTitle>
            </EuiPageContentHeaderSection>
        </EuiPageContentHeader>
        <EuiPageContentBody>Content body</EuiPageContentBody>
    </EuiPageContent>
)

export default MainPage
