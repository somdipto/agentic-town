
from flask import Flask, render_template, jsonify
import matplotlib.pyplot as plt
import io
import base64
from simulation.model import run_simulation
import pandas as pd

app = Flask(__name__)

scenario_config = {
    "num_agents": 10,
    "simulation_days": 30,
    "initial_skills": {
        "farming": {"range": (1, 10)},
        "crafting": {"range": (1, 10)},
        "gathering": {"range": (1, 10)}
    },
    "environment_setup": {
        "resources": {
            "food": 100,
            "wood": 50,
            "stone": 30
        },
        "landscape": "forest_village"
    },
    "agent_types": {
        "farmer": {"focus": "farming", "energy_multiplier": 1.2},
        "craftsman": {"focus": "crafting", "energy_multiplier": 1.1},
        "gatherer": {"focus": "gathering", "energy_multiplier": 1.3}
    },
    "event_schedule": [
        {"day": 5, "type": "resource_boost", "details": {"resource": "food", "amount": 20}},
        {"day": 15, "type": "weather_event", "details": {"weather": "rain", "duration": 3}}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run')
def run():
    simulation_df = run_simulation(scenario_config)

    # Data aggregation and visualization
    skills_df = pd.json_normalize(simulation_df['skills'])
    skills_df.columns = [f'skill_{col}' for col in skills_df.columns]
    simulation_df_unnested = pd.concat([simulation_df.drop('skills', axis=1), skills_df], axis=1)

    daily_avg_metrics = simulation_df_unnested.groupby('day').agg(
        average_age=('age', 'mean'),
        average_energy=('energy', 'mean'),
        average_farming_skill=('skill_farming', 'mean'),
        average_crafting_skill=('skill_crafting', 'mean'),
        average_gathering_skill=('skill_gathering', 'mean')
    ).reset_index()

    # Generate plots
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    axes[0].plot(daily_avg_metrics['day'], daily_avg_metrics['average_age'], marker='o', linestyle='-')
    axes[0].set_title('Average Age Over Time')
    axes[0].set_xlabel('Day')
    axes[0].set_ylabel('Average Age')
    axes[0].grid(True)

    axes[1].plot(daily_avg_metrics['day'], daily_avg_metrics['average_energy'], marker='o', linestyle='-', color='orange')
    axes[1].set_title('Average Energy Over Time')
    axes[1].set_xlabel('Day')
    axes[1].set_ylabel('Average Energy')
    axes[1].grid(True)

    axes[2].plot(daily_avg_metrics['day'], daily_avg_metrics['average_farming_skill'], marker='o', linestyle='-', label='Farming')
    axes[2].plot(daily_avg_metrics['day'], daily_avg_metrics['average_crafting_skill'], marker='o', linestyle='-', label='Crafting')
    axes[2].plot(daily_avg_metrics['day'], daily_avg_metrics['average_gathering_skill'], marker='o', linestyle='-', label='Gathering')
    axes[2].set_title('Average Skill Levels Over Time')
    axes[2].set_xlabel('Day')
    axes[2].set_ylabel('Average Skill Level')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    
    # Save plot to a string
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')

    return render_template('results.html', plot_url=plot_url, tables=[daily_avg_metrics.to_html(classes='data')])

if __name__ == '__main__':
    app.run(debug=True)
