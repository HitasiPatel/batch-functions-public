## Deploying Batch Orchestrator Code
1. The batch orhchestrator code is part of the `av-batch-orchestrator` folder under main repo.
2. Checkout the code and create a file named `.env` under `av-batch-orchestrator\app` folder.
3. There is a file named `env.template` under the root directory of the batch orchestrartor. Copy contents of this file into the `.env` file.
4. Fill in the values for all the properties in `.env` file.
5. We need SAS keys to connect to the storage accounts. Here are the steps to generate a SAS key:
    * Open Azure Portal and access the storage account.
    * Click `Shared access signature` option under left side menu.
    * Select allowed resource types and set the expiry date as needed.
    * Click on `Generate sas and connection string button` to generate the SAS key.
    * Sample screenshot is shown below:
    ![Batch pool application](images/app-step3.png)

6. Create a zip folder with app folder and requirements.txt inside it.
7. Create an application with name batch-orchestrator and version 1.0 under the Batch Account in the Azure Portal.

    ![Batch pool application](images/app-step1.png)

8. Upload the zip folder created in step 6, to the application created in step 7.

9. If application code has to be updated, use update option under the application.

    ![Batch pool application](images/app-step2.png)
10. For detailed instructions read [this documentation](https://learn.microsoft.com/en-us/azure/batch/batch-application-packages)

11. Important note: Orchestration and execution pools have number of nodes set to zero by default, to save on costs. When solution has to be used, scale both the pools to appropriate size on Azure Portal. One node per each pool should be good enough for the test data provided in this solution kit.
