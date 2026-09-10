# from fastapi import HTTPException, status

# from app.repositories.customer_policy_repository import (
#     CustomerPolicyRepository,
# )


# class CustomerPolicyService:

#     @staticmethod
#     def get_policy():

#         policy = (
#             CustomerPolicyRepository
#             .get_active_policy()
#         )

#         if not policy:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Active customer policy not found.",
#             )

#         return {
#             "success": True,
#             "item": policy,
#             "message": (
#                 "Customer policies fetched successfully."
#             ),
#         }




















from fastapi import HTTPException, status

from app.repositories.customer_policy_repository import (
    CustomerPolicyRepository,
)


class CustomerPolicyService:

    @staticmethod
    def get_policy():

        policy = (
            CustomerPolicyRepository
            .get_active_policy()
        )

        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Active customer policy not found.",
            )

        return {
            "success": True,
            "item": policy,
            "message": (
                "Customer policies fetched successfully."
            ),
        }