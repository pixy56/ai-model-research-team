name: Research Team Issue

description: Create a new story or task for the AI Model Research Team

title: "[Story] "

labels: []

body:
  - type: markdown
    attributes:
      value: |
        ## Story/Task Template
        
        Use this template to create new work items for the research team.

  - type: dropdown
    id: story-type
    attributes:
      label: Story Type
      options:
        - Literature Review
        - Data Analysis
        - Writing
        - Integration
        - Dev Team
        - Other
    validations:
      required: true

  - type: input
    id: story-points
    attributes:
      label: Story Points
      description: Estimated effort (1, 2, 3, 5, 8, 13)
      placeholder: "3"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Description
      description: What needs to be done?
      placeholder: Describe the story/task...
    validations:
      required: true

  - type: textarea
    id: acceptance-criteria
    attributes:
      label: Acceptance Criteria
      description: What defines "done"?
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
        - [ ] Criterion 3
    validations:
      required: true

  - type: textarea
    id: dependencies
    attributes:
      label: Dependencies
      description: Any dependencies or blockers?
      placeholder: None

  - type: dropdown
    id: iteration
    attributes:
      label: Target Iteration
      options:
        - Iteration 1 (Foundation)
        - Iteration 2 (Data Collection)
        - Iteration 3 (Analysis)
        - Iteration 4 (Insights)
        - Iteration 5 (Synthesis)
        - Future
    validations:
      required: true