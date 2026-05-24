import { gql } from "@apollo/client";

export const RECOMMENDATION_ITEM_FRAGMENT = gql`
  fragment RecommendationItemSummary on RecommendationItemType {
    publicId
    foodPublicId
    rank
    score
    isExploration
  }
`;
