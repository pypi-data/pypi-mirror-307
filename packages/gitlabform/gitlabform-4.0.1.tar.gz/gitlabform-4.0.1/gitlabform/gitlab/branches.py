from gitlabform.gitlab.core import GitLabCore, NotFoundException


class GitLabBranches(GitLabCore):
    def protect_branch(self, project_and_group_name, branch, protect_settings):
        url = "projects/%s/protected_branches?name=%s"
        parameters_list = [
            project_and_group_name,
            branch,
        ]
        return self._make_requests_to_api(
            url,
            tuple(parameters_list),
            method="POST",
            expected_codes=[
                200,
                201,
            ],
            json=protect_settings,
        )

    def set_branch_code_owner_approval_required(
        self,
        project_and_group_name,
        branch,
        code_owner_approval_required,
    ):
        data = {
            "id": project_and_group_name,
            "branch": branch,
            "code_owner_approval_required": code_owner_approval_required,
        }
        return self._make_requests_to_api(
            "projects/%s/protected_branches/%s",
            (
                project_and_group_name,
                branch,
            ),
            method="PATCH",
            data=data,
            expected_codes=[200, 201],
        )

    def unprotect_branch(self, project_and_group_name, branch):
        # 404 means that the branch is already unprotected
        return self._make_requests_to_api(
            "projects/%s/protected_branches/%s",
            (project_and_group_name, branch),
            method="DELETE",
            expected_codes=[200, 201, 204, 404],
        )

    def get_branches(self, project_and_group_name):
        result = self._make_requests_to_api(
            "projects/%s/repository/branches", project_and_group_name
        )
        return sorted(map(lambda x: x["name"], result))

    def get_branch(self, project_and_group_name, branch):
        return self._make_requests_to_api(
            "projects/%s/repository/branches/%s", (project_and_group_name, branch)
        )

    def get_branch_access_levels(self, project_and_group_name, branch):
        return self._make_requests_to_api(
            "projects/%s/protected_branches/%s", (project_and_group_name, branch)
        )

    def create_branch(
        self, project_and_group_name, new_branch_name, create_branch_from_ref
    ):
        data = {
            "id": project_and_group_name,
            "branch": new_branch_name,
            "ref": create_branch_from_ref,
        }
        self._make_requests_to_api(
            "projects/%s/repository/branches",
            project_and_group_name,
            method="POST",
            data=data,
            expected_codes=[200, 201],
        )

    def delete_branch(self, project_and_group_name, branch):
        self._make_requests_to_api(
            "projects/%s/repository/branches/%s",
            (project_and_group_name, branch),
            method="DELETE",
            expected_codes=[200, 204],
        )

    def get_protected_branches(self, project_and_group_name):
        protected_branches = self._make_requests_to_api(
            "projects/%s/protected_branches", project_and_group_name
        )
        return [branch["name"] for branch in protected_branches]

    def get_unprotected_branches(self, project_and_group_name):
        branches = self._make_requests_to_api(
            "projects/%s/repository/branches", project_and_group_name
        )

        unprotected_branches = []
        for branch in branches:
            if not branch["protected"]:
                name = branch["name"]
                unprotected_branches.append(name)

        return unprotected_branches
