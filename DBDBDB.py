import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import * as pd from 'pandas-js';

// CSV 데이터를 가져오는 함수
const fetchCSVData = async () => {
  try {
    const response = await fetch('/api/hr-data'); // API 엔드포인트 가정
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch CSV data:", error);
    return [];
  }
};

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const csvData = await fetchCSVData();
        setData(csvData);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const processRoleYearDistribution = () => {
    if (data.length === 0) return [];
    
    const df = new pd.DataFrame(data);
    const grouped = df.groupby(['년도', '역할구분 (MPRS)']).size().reset_index();
    grouped.columns = ['년도', '역할구분 (MPRS)', 'count'];
    
    const pivoted = grouped.pivot({ 
      index: '년도', 
      columns: '역할구분 (MPRS)', 
      values: 'count' 
    }).reset_index();
    
    return pivoted.to_json({ orient: 'records' });
  };

  const processFemaleRatios = () => {
    if (data.length === 0) return [];
    
    const df = new pd.DataFrame(data);
    const total = df.groupby(['년도', '역할구분 (MPRS)']).size().reset_index();
    total.columns = ['년도', '역할구분 (MPRS)', 'total'];
    
    const female = df[df['성별'] === '여'].groupby(['년도', '역할구분 (MPRS)']).size().reset_index();
    female.columns = ['년도', '역할구분 (MPRS)', 'female'];
    
    const merged = total.merge(female, on=['년도', '역할구분 (MPRS)'], how='left');
    merged['female_ratio'] = (merged['female'] / merged['total']) * 100;
    
    const pivoted = merged.pivot({ 
      index: '년도', 
      columns: '역할구분 (MPRS)', 
      values: 'female_ratio' 
    }).reset_index();
    
    return pivoted.to_json({ orient: 'records' });
  };

  const process2024GenderDistribution = () => {
    if (data.length === 0) return [];
    
    const df = new pd.DataFrame(data);
    const filtered = df[df['년도'] === 2024];
    const grouped = filtered.groupby(['역할구분 (MPRS)', '성별']).size().reset_index();
    grouped.columns = ['역할구분 (MPRS)', '성별', 'count'];
    
    const pivoted = grouped.pivot({ 
      index: '역할구분 (MPRS)', 
      columns: '성별', 
      values: 'count' 
    }).reset_index();
    pivoted.columns = ['name', 'male', 'female'];
    
    return pivoted.to_json({ orient: 'records' });
  };

  const roleYearDistribution = processRoleYearDistribution();
  const femaleRatios = processFemaleRatios();
  const genderDistribution2024 = process2024GenderDistribution();

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">HR Data Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>연도별 역할 분포</CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={roleYearDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="년도" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="M" fill="#8884d8" />
                <Bar dataKey="P" fill="#82ca9d" />
                <Bar dataKey="R" fill="#ffc658" />
                <Bar dataKey="S" fill="#ff7300" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>연도별 여성 비율</CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={femaleRatios}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="년도" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="M" fill="#8884d8" />
                <Bar dataKey="P" fill="#82ca9d" />
                <Bar dataKey="R" fill="#ffc658" />
                <Bar dataKey="S" fill="#ff7300" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardHeader>2024년 역할별 성별 분포</CardHeader>
          <CardContent>
            <div className="flex justify-around">
              {genderDistribution2024.map((entry, index) => (
                <div key={entry.name} className="text-center">
                  <h3 className="font-bold">{entry.name}</h3>
                  <ResponsiveContainer width={100} height={100}>
                    <PieChart>
                      <Pie
                        data={[
                          { name: 'Male', value: entry.male },
                          { name: 'Female', value: entry.female }
                        ]}
                        cx="50%"
                        cy="50%"
                        innerRadius={30}
                        outerRadius={50}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {
                          [{ name: 'Male', value: entry.male }, { name: 'Female', value: entry.female }].map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))
                        }
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                  <div>Male: {entry.male}</div>
                  <div>Female: {entry.female}</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
