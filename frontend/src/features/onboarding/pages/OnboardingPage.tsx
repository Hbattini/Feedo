import { useReducer } from "react";

type OnboardingState = {
  step: "cat_profile" | "preferences" | "review";
  draftCatName: string;
};

type OnboardingAction =
  | { type: "set_cat_name"; value: string }
  | { type: "go_to_preferences" }
  | { type: "go_to_review" };

const initialState: OnboardingState = {
  step: "cat_profile",
  draftCatName: ""
};

function onboardingReducer(state: OnboardingState, action: OnboardingAction): OnboardingState {
  switch (action.type) {
    case "set_cat_name":
      return { ...state, draftCatName: action.value };
    case "go_to_preferences":
      return { ...state, step: "preferences" };
    case "go_to_review":
      return { ...state, step: "review" };
  }
}

export function OnboardingPage() {
  const [state, dispatch] = useReducer(onboardingReducer, initialState);

  return (
    <main className="page stack">
      <h1>Onboarding</h1>
      <section className="panel stack">
        <p className="muted">Current step: {state.step}</p>
        <label>
          Cat name
          <input
            value={state.draftCatName}
            onChange={(event) => dispatch({ type: "set_cat_name", value: event.target.value })}
          />
        </label>
        <button
          className="button"
          type="button"
          onClick={() => dispatch({ type: "go_to_preferences" })}
        >
          Continue
        </button>
      </section>
    </main>
  );
}
