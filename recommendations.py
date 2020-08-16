
class RecommendationCustomSystem:

    @staticmethod
    def get_recommendations_by_custom(user, quantity):

        return list(range(1, quantity))


    @staticmethod
    def get_recommendations_by_group(user, quantity, group_criteria):

        return list(range(1, quantity))
