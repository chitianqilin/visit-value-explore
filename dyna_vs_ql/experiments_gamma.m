clear all
do_plot = 0;
long_horizon = 0;
optimistic = 0;
mdp_name = ["Taxi"];
% mdp_name = ["GridworldSparseSmall"];

for gamma_vv = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.99999]
    for trial = 1 : 20
        fprintf('%f %d\n', gamma_vv, trial)
        for alg_name = [ ...
                "vv_n_classic", ...
                "vv_ucb_classic", ...
                ]
            feval(['run_ql_' char(alg_name)])
            save([setting_str '/' char(alg_name) '_' num2str(gamma_vv*100) '_' num2str(trial) '.mat'], save_list{:})
        end
    end
end
