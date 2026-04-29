import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle

df = pd.read_csv('../dataset.csv')

# Duration is maybe unnecessary as the delays that were simulated don't differentiate that much
required_fields = [ 'label', 'bidirectional_packets', 
                    'src2dst_packets',  'dst2src_packets', 'bidirectional_syn_packets',
                    'bidirectional_ack_packets', 'bidirectional_psh_packets', 'src2dst_syn_packets', 'src2dst_ack_packets', 'src2dst_psh_packets',
                    'dst2src_syn_packets', 'dst2src_ack_packets', 'dst2src_psh_packets', 
                     'dst2src_rst_packets', 'src2dst_rst_packets' ]

# Duration variables, might be compromised due to difference of tools
# 'bidirectional_duration_ms', 'src2dst_duration_ms', 'dst2src_duration_ms', 

# Removed due to size fingerprinting caused by different tools
# 'dst2src_min_ps' 'src2dst_min_ps' 'src2dst_mean_ps' 'src2dst_max_ps', 'dst2src_max_ps', 'dst2src_mean_ps', 'src2dst_bytes', 'dst2src_bytes', 'bidirectional_bytes',

# Split dataframes according to their purpose
df_learning = df[df['split'] == 'learning']
df_validating = df[df['split'] == 'validating']
df_testing = df[df['split'] == 'testing']

df_learning = shuffle(df_learning[required_fields])
df_validating = df_validating[required_fields]
df_testing = shuffle(df_testing[required_fields])

X_train = df_learning.iloc[:, 1:len(required_fields)]
y_train = df_learning.iloc[:, 0]

X_test = df_testing.iloc[:, 1:len(required_fields)]
y_test = df_testing.iloc[:, 0]

rf = RandomForestClassifier()
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print(rf.score(X_test, y_test))

features = pd.Series(
    rf.feature_importances_,
    index=X_train.columns
).sort_values(ascending=False)
print(features)

