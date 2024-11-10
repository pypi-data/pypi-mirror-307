import argparse
import os
from .utils import sample_data
from .generation_1 import generate_topic_lvl1
from .generation_2 import generate_topic_lvl2
from .refinement import refine_topics
from .assignment import assign_topics
from .correction import correct_topics

def pipeline(input_file, input_sample_size, seed_topic_file, api, model, verbose, apply_refinement, generate_subtopics):
    """
    End-to-end TopicGPT pipeline
    """
    ## Generation I/O
    base_path = os.path.abspath(os.path.dirname(__file__))
    data_name = os.path.splitext(os.path.basename(input_file))[0]
    output_dir = os.path.join(base_path, "data", "output", data_name)
    os.makedirs(output_dir, exist_ok=True)
    
    generation_prompt = os.path.join(base_path, "prompt", "generation_1.txt")
    seed_1 = os.path.join(base_path, "prompt", "seed_1.md")
    generation_out = os.path.join(output_dir, "generation_1.jsonl")
    generation_topic = os.path.join(output_dir, "generation_1.md")

    # Refinement I/O
    refinement_prompt = os.path.join(base_path, "prompt", "refinement.txt")
    refinement_out = os.path.join(output_dir, "refinement.jsonl")
    refinement_topic = os.path.join(output_dir, "refinement.md")
    refinement_mapping = os.path.join(output_dir, "refinement_mapping.txt")
    refinement_updated = os.path.join(output_dir, "refinement_updated.jsonl")

    # Generation 2 I/O
    generation_2_prompt = os.path.join(base_path, "prompt", "generation_2.txt")
    generation_2_out = os.path.join(output_dir, "generation_2.jsonl")
    generation_2_topic = os.path.join(output_dir, "generation_2.md")

    ## Assignment I/O
    assignment_prompt = os.path.join(base_path, "prompt", "assignment.txt")
    assignment_out = os.path.join(output_dir, "assignment.jsonl")

    ## Correction I/O
    correction_prompt = os.path.join(base_path, "prompt", "correction.txt")
    correction_out = os.path.join(output_dir, "assignment_corrected.jsonl")

    if verbose:
        print("-----------------------------------")
        print("Initiating TopicGPT pipeline")
        print("Input sample size: ", input_sample_size)
        print("Seed topic file: ", seed_topic_file)
        print("API: ", api)
        print("Model: ", model)
        print("Apply refinement: ", apply_refinement)
        print("Generate subtopics: ", generate_subtopics)
        print("-----------------------------------")

    if input_sample_size: 
        input_sample_out = os.path.splitext(input_file)[0] + "_sample.jsonl"
        sample_data(os.path.join(base_path, input_file), input_sample_size, input_sample_out)
        if verbose: print("Input sample file: ", input_sample_out)
    else: 
        input_sample_out = input_file

    # Generate topics (lvl 1)
    generate_topic_lvl1(api, model, input_sample_out, generation_prompt, seed_1, generation_out, generation_topic, True)

    # Refinement
    if apply_refinement: 
        refine_topics(api, model, refinement_prompt, 
                      generation_out, generation_topic, 
                    refinement_topic, refinement_out,
                    verbose=verbose, 
                    remove=True, 
                    mapping_file=refinement_mapping,
                    refined_again=False)
    
    # Generate topics (lvl 2)
    if generate_subtopics:
        generate_topic_lvl2(api, model, 
                    generation_topic, 
                    generation_out, 
                    generation_2_prompt, 
                    generation_2_out, 
                    generation_2_topic, 
                    verbose=True)
        
    # Assign topics
    assign_topics(api, model, input_sample_out, assignment_prompt, 
                  assignment_out, generation_topic, verbose=verbose)
    
    # Correct topics
    correct_topics(api, model, assignment_out, correction_prompt, generation_topic, correction_out, verbose=verbose)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='End-to-end TopicGPT pipeline')
    parser.add_argument('--input_file', type=str, help='Input text file')
    parser.add_argument('--input_sample_size', type=int, help='Input sample size')
    parser.add_argument('--seed_topic_file', type=str, help='Seed topic file')

    parser.add_argument('--api', type=str, help='API name')
    parser.add_argument('--model', type=str, help='Model name')

    parser.add_argument('--verbose', type=bool, help='Verbose mode', default=True)
    parser.add_argument('--apply_refinement', type=bool, help='Apply refinement', default=False)
    parser.add_argument('--generate_subtopics', type=bool, help='Generate subtopics', default=False)

    args = parser.parse_args()

    pipeline(args.input_file, args.input_sample_size, args.seed_topic_file, args.api, args.model, args.verbose, args.apply_refinement, args.generate_subtopics)
