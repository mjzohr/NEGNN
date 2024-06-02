import os
import sys

from tqdm import tqdm
from utils.train_nc import main
from utils.utils import set_seed, test_settings_similarity



def run_experiments(seed, dataset_name, model_name, extend_metric):
    set_seed(seed)

    gamma = explore = alpha = beta = gamma = 1
    results_file = f"results/node_classification/similarity/{dataset_name}_{model_name}_{seed}_{extend_metric}.txt"

    org_accuracy, org_precision, org_recall, org_f1 = main(seed=seed, dataset_name=dataset_name, extend_metric='None', model_name=model_name, alpha=alpha, beta=beta, gamma=gamma, explore=explore)
    with open(results_file, 'w') as f:
        f.write(f"Original {model_name} on {dataset_name} with seed: {seed}, extend metric: {extend_metric}")
        f.write("\n")
        f.write(f"accuracy, precision, recall, f1, alpha, gamma, explore")
        f.write("\n")
        f.write("{:.3f},{:.3f},{:.3f},{:.3f},{},{}".format(org_accuracy, org_precision, org_recall, org_f1, alpha, gamma, explore))
        f.write("\n")
        f.write("Experiments started")
        f.write("\n--------------------------------------------\n")

    test_list_alpha_similarity, test_list_gamma, test_list_explore = test_settings_similarity(dataset_name)
    beta = 0
    for explore in test_list_explore:
        for alpha in test_list_alpha_similarity:
            for gamma in tqdm(test_list_gamma):
                accuracy, precision, recall, f1 = main(seed=seed, dataset_name=dataset_name, model_name=model_name, alpha=alpha, beta=beta, gamma=gamma, explore=explore, extend_metric=extend_metric)

                # if (accuracy > org_accuracy) or (f1 > org_f1):
                with open(results_file, 'a') as f:
                    f.write("{:.3f},{:.3f},{:.3f},{:.3f},{},{}".format(accuracy, precision, recall, f1, alpha, gamma, explore))
                    f.write("\n")




if __name__ == "__main__":
    # Centrality runs 
    os.makedirs('results/node_classification/similarity/', exist_ok=True)

    seeds = [1]
    # seeds = [1, 2, 3, 4, 5]
    dataset_names = ['cora', 'citeseer', 'pubmed', 'amazonphoto', 'amazoncomputer']
    model_names = ['gat', 'gatv2', 'gcn', 'sage']
    extend_metrics = ["adamic_adar", "jaccard", "resource_allocation"]

    for seed in seeds:
        for dataset_name in tqdm(dataset_names):
            for model_name in model_names:
                for extend_metric in extend_metrics:
                    run_experiments(seed, dataset_name, model_name, extend_metric)