import { gql } from "@apollo/client";

import { RECOMMENDATION_ITEM_FRAGMENT } from "../fragments/recommendation";

export const RECOMMENDATIONS_FOR_CAT_QUERY = gql`
  ${RECOMMENDATION_ITEM_FRAGMENT}
  query RecommendationsForCat($catPublicId: ID!, $limit: Int!) {
    recommendationsForCat(catPublicId: $catPublicId, limit: $limit) {
      publicId
      catPublicId
      ruleVersion
      generatedAt
      items {
        ...RecommendationItemSummary
      }
    }
  }
`;
