import { gql } from "@apollo/client";

export const GENERATE_RECOMMENDATIONS_MUTATION = gql`
  mutation GenerateRecommendationsForCat($catPublicId: ID!, $limit: Int!) {
    generateRecommendationsForCat(catPublicId: $catPublicId, limit: $limit) {
      publicId
      catPublicId
      ruleVersion
      generatedAt
    }
  }
`;

export const SUBMIT_RECOMMENDATION_FEEDBACK_MUTATION = gql`
  mutation SubmitRecommendationFeedback($data: RecommendationFeedbackInput!) {
    submitRecommendationFeedback(data: $data)
  }
`;
